import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from csv import DictWriter
from enum import Enum
import json
import logging
import sys
from multiprocessing import Lock

import numpy as np

from howso.utilities.monitors import Timer


class GameType(str, Enum):
    WTM = "wtm"
    CART_POLE = "cartpole"

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return list(map(lambda c: c.value, cls))


class Simulation:

    def __init__(self, iterations=1, max_workers=1):
        self.max_workers = max(1, max_workers)
        self.iterations = max(1, iterations)

    @classmethod
    def process_args(cls, arguments):
        """Process command line arguments."""
        parser = argparse.ArgumentParser(
            description='Play a reinforcement learning game.')
        parser.add_argument(
            'game_type', default=GameType.WTM, nargs='?',
            choices=GameType.choices(),
            help='The game type to play.')
        parser.add_argument(
            'agent_type', default='basic', nargs='?',
            choices=['basic', 'time-series'],
            help='The agent type to use to play the game. (Not all games '
                 'support all agents)')
        parser.add_argument(
            '--iterations', '-i', dest='iterations', type=int, default=1,
            help='The number of times to run the simulation.')
        parser.add_argument(
            '--workers', '-w', dest='workers', type=int, default=1,
            help='The number of workers to use to play the game.')
        parser.add_argument(
            '--explanation', '-e', dest='explanation_level', type=int,
            default=1, help='The explanation level to use when reacting.')
        parser.add_argument(
            '--seed', '-s', dest='seed', type=int, default=argparse.SUPPRESS,
            help='The Gym seed.')
        parser.add_argument(
            '--max-rounds', dest='max_rounds', type=int,
            default=argparse.SUPPRESS,
            help='The maximum number of rounds to attempt at winning the game.')
        parser.add_argument(
            '--render-mode', dest='render_mode', default=argparse.SUPPRESS,
            help='The Gym render mode. (Not all games support all '
                 'render modes)')
        parser.add_argument(
            '--log-level', dest='log_level', default=logging.INFO,
            help="The the log level to use.")
        parser.add_argument(
            '--csv', dest='csv', metavar='FILE', type=str,
            help="Append results to FILE")
        parser.add_argument(
            '--configuration', dest='configuration', type=str,
            help="Record CONFIGURATION in CSV-format output")

        return parser.parse_args(arguments)

    @classmethod
    def entrypoint(cls, arguments):
        """CLI entrypoint."""
        args = vars(cls.process_args(arguments))
        logging.basicConfig(stream=sys.stdout, level=args.pop('log_level'),
                            format="[%(asctime)s] %(levelname)s: %(message)s")
        sim = cls(args.pop('iterations'), max_workers=args.pop('workers'))
        csvname = args.pop('csv')
        configuration = args.pop('configuration')
        result = sim.run(**args)

        # Output results
        runs = result['runs']
        metrics = result['metrics']
        percent_won = metrics['percent-won']
        total_won = metrics['total-won']
        avg_win_rounds = metrics['average-rounds-to-win']
        avg_win_cases = metrics['average-win-cases']
        avg_win_high_score = metrics['average-win-high-score']
        avg_win_duration = metrics['average-win-duration']

        print(json.dumps(runs, indent=4, sort_keys=True, default=str))
        print(f"Summary:\n"
              f"    Game type: {args.get('game_type')}\n"
              f"    Agent type: {args.get('agent_type')}\n"
              f"    Total iterations: {len(runs)}\n"
              f"    Winning iterations: {total_won}\n"
              f"    Percentage of winners: {percent_won:.1f}\n"
              f"    Avg. rounds required to win: {avg_win_rounds:.1f}\n"
              f"    Avg. cases required to win: {avg_win_cases:.1f}\n"
              f"    Avg. winning game high score: {avg_win_high_score:.1f}\n"
              f"    Avg. winning game duration: {avg_win_duration}\n"
              f"    Elapsed time: {result['duration']}")

        if csvname:
            with open(csvname, 'a', newline='') as csvfile:
                writer = DictWriter(
                    csvfile,
                    ['game_type', 'agent_type', 'configuration', 'iteration', 'win', 'rounds', 'high_score',
                     'total_cases', 'duration']
                )
                if csvfile.tell() == 0:
                    writer.writeheader()
                for iteration, run in runs.items():
                    writer.writerow({
                        'game_type': args.get('game_type'),
                        'agent_type': args.get('agent_type'),
                        'configuration': configuration,
                        'iteration': int(iteration),
                        'win': 'true' if run['win'] else 'false',
                        'rounds': run['rounds'],
                        'high_score': run['high_score'],
                        'total_cases': run['total_cases'],
                        'duration': run['duration'].total_seconds()
                    })

    @staticmethod
    def _process_initializer(lock, logger):
        """Initialize the HowsoClient once for each process."""
        with lock:
            # This instantiates the underlying HowsoClient instance which
            # may write/read from the file system so we do so in a lock
            try:
                from howso import engine
                engine.get_client()
            except Exception:
                logger.exception('Failed to instantiate client in initializer')

    def run(self, **kwargs):
        """Run the game across multiple processes."""
        runs = {}

        logger = logging.getLogger('howso.rl.examples')
        logger.info(f"Running {self.iterations} {kwargs.get('agent_type')} "
                    f"simulations of {kwargs.get('game_type')} with "
                    f"{self.max_workers} workers")

        with Timer() as timer:
            if self.max_workers == 1:
                for i in range(self.iterations):
                    runs[i] = self.run_single(i, **kwargs)
            else:
                lock = Lock()
                pool = ProcessPoolExecutor(max_workers=self.max_workers,
                                           initializer=self._process_initializer,
                                           initargs=[lock, logger])
                tasks = {}
                try:
                    tasks = {
                        pool.submit(self.run_single, i, **kwargs): i
                        for i in range(self.iterations)
                    }
                    for future in as_completed(tasks):
                        iteration = tasks[future]
                        runs[iteration] = result = future.result()
                        logger.info('Iteration %.0f finished: win=%s rounds=%s',
                                    iteration, result['win'], result['rounds'])
                except KeyboardInterrupt:
                    for task in tasks:
                        task.cancel()
                    pool.shutdown(wait=False)
                    exit()

        logger.info(
            f'Completed {self.iterations} simulations in {timer.duration}')
        return {
            'runs': runs,
            'duration': timer.duration,
            'metrics': self.get_metrics(runs)
        }

    def run_single(self, iteration: int, *, game_type: str, **kwargs):
        """Run a single simulation of a game."""
        # Import locally so loggers are created after setup
        GameClass = import_game(game_type)
        # force a random seed for every iteration
        if "seed" not in kwargs:
            kwargs["seed"] = (1 + iteration) * int(100000 * np.random.rand())
        with GameClass(**kwargs) as game:
            result = game.play()
        return result

    def get_metrics(self, runs):
        """Calculate and return metrics for given runs."""
        total_won = sum([1 for v in runs.values() if v['win']])
        percent_won = (100.0 * total_won / len(runs))
        if total_won > 0:
            avg_win_high_score = np.mean(
                [v['high_score'] for v in runs.values() if v['win']])
            avg_win_duration = np.mean(
                [v['duration'] for v in runs.values() if v['win']])
            avg_win_cases = np.mean(
                [v['total_cases'] for v in runs.values() if v['win']])
            avg_win_rounds = np.mean(
                [v['rounds'] for v in runs.values() if v['win']])
        else:
            avg_win_high_score = float("nan")
            avg_win_duration = float("nan")
            avg_win_cases = float("nan")
            avg_win_rounds = float("nan")

        return {
            'total-won': total_won,
            'percent-won': percent_won,
            'average-rounds-to-win': avg_win_rounds,
            'average-win-high-score': avg_win_high_score,
            'average-win-duration': avg_win_duration,
            'average-win-cases': avg_win_cases
        }


def import_game(game_type: GameType):
    """
    Import a game implementation given a game_type.

    Games are imported during runtime so loggers are created after setup.

    Parameters
    ----------
    game_type : GameType
        The type of game to import.

    Raises
    ------
    ValueError
        When the game type is not valid.
    """
    if game_type == GameType.WTM:
        from .wafer_thin_mint.game import WaferThinMintGame as Game
    elif game_type == GameType.CART_POLE:
        from .cart_pole.game import CartPoleGame as Game
    else:
        raise ValueError("Invalid game type")

    return Game
