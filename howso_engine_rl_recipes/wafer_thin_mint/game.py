import logging

from howso.utilities.monitors import Timer
import numpy as np

from ..common.game import BaseGame, GameResult
from .agent import agent_registry

logger = logging.getLogger('howso.rl.examples.wafer_thin_mint')


class WaferThinMintGame(BaseGame):
    """
    Play the cart pole game.

    Considered solved when the maximum score is achieved 100 consecutive rounds.
    """

    game_id = 'WaferThinMint-v0'
    win_threshold = 6  # Required average score across all rounds to consider the game won

    def __init__(self, agent_type: str, **kwargs) -> None:
        try:
            agent = agent_registry[agent_type]
        except KeyError:
            raise ValueError("Invalid agent type. Allowed types include: "
                             f"[{', '.join(agent_registry.keys())}]")
        kwargs.setdefault("max_rounds", 150)
        super().__init__(agent, **kwargs)

    def play(self) -> GameResult:
        """Play the game."""
        observation, _ = self.env.reset(seed=self.seed)
        agent = self.agent_class(
            env=self.env,
            explanation_level=self.explanation_level,
            seed=self.seed,
            win_threshold=self.win_threshold,
        )
        agent.setup()

        round_num = 1
        step = 1
        highest_score = 0
        final_scores = []
        round_score = 0
        is_win = False
        total_cases = 0

        timer = Timer()
        timer.start()

        while True:
            if round_num > self.max_rounds:
                avg_score = np.mean(final_scores)
                if avg_score >= self.win_threshold:
                    logger.info(f"Game won after {self.max_rounds} games with an average score of {avg_score:.3f}")
                    is_win = True
                else:
                    logger.error(
                        f"Failed to win within {self.max_rounds} games with an average score of {avg_score:.3f}")
                break

            action = agent.act(observation, round_num, step)
            logger.debug("Act: %s", action)
            observation, reward, terminated, truncated, _ = self.env.step(action)

            if reward == -1:
                # If they've hit the 'explosion threshold' assign low score
                round_score = -10
            else:
                # Otherwise assign the step reward
                round_score += reward

            if terminated or truncated:
                # Game has ended
                logger.debug('Terminated %s:%s ob=%s',
                             round_num, step, observation)
                final_scores.append(round_score)

                agent.assign_reward(observation, final_scores, round_num, step)

                observation, _ = self.env.reset()
                highest_score = max(highest_score, round_score)
                round_score = 0
                step = 1
                round_num += 1
                logger.debug("Game env reset")
            else:
                logger.debug('Step %s:%s ob=%s', round_num, step, observation)
                step += 1

        # Capture total number of trained cases
        if hasattr(agent, 'trainee'):
            total_cases = agent.trainee.get_num_training_cases()

        agent.done(is_win)
        timer.end()
        return {
            'win': is_win,
            'rounds': len(final_scores),
            'high_score': highest_score,
            'duration': timer.duration,
            'total_cases': total_cases,
            'average_score': float(np.mean(final_scores)),
        }
