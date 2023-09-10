import logging

from howso.utilities.monitors import Timer
import numpy as np

from ..common.game import BaseGame, GameResult
from .agent import agent_registry

logger = logging.getLogger('howso.rl.examples.cart_pole')


class CartPoleGame(BaseGame):
    """
    Play the cart pole game.

    https://gymnasium.farama.org/environments/classic_control/cart_pole/

    Considered solved when the average reward is greater than or equal to
    195.0 over 100 consecutive rounds.
    """

    game_id = 'CartPole-v1'
    win_threshold = 100  # Required number of rounds to solve
    required_average = 195  # Required average score to solve

    def __init__(self, agent_type: str, **kwargs) -> None:
        try:
            agent = agent_registry[agent_type]
        except KeyError:
            raise ValueError("Invalid agent type. Allowed types include: "
                             f"[{', '.join(agent_registry.keys())}]")
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
        final_scores = []
        round_score = 0
        highest_score = 0
        total_cases = 0
        is_win = False

        timer = Timer()
        timer.start()

        while True:
            if round_num >= self.max_rounds:
                logger.error(f"Failed to win within {round_num} games")
                break

            action = agent.act(observation, round_num, step)
            logger.debug("Act: %s", action)
            observation, reward, terminated, truncated, _ = self.env.step(action)
            round_score += reward

            if terminated or truncated:
                # Game has been lost
                logger.debug('Terminated %s:%s ob=%s',
                             round_num, step, observation)
                final_scores.append(round_score)

                if (
                    len(final_scores) >= self.win_threshold and
                    np.mean(final_scores[-self.win_threshold:]) >= self.required_average
                ):
                    logger.info(f"Game won after {round_num} games with a high "
                                f"score of {highest_score}")
                    is_win = True
                    break
                else:
                    agent.assign_reward(
                        observation, final_scores, round_num, step)

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
            'rounds': round_num,
            'total_average_score': float(np.mean(final_scores)),
            'average_score': float(np.mean(final_scores[-self.win_threshold:])),
            'high_score': highest_score,
            'total_cases': total_cases,
            'duration': timer.duration
        }
