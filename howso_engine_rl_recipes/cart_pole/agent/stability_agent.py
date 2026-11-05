import logging

import numpy as np

from .basic_agent import BasicAgent

logger = logging.getLogger('howso.rl.examples.cart_pole')


class StabilityAgent(BasicAgent):
    """
    Cart-Pole stability-shaped agent.

    Identical to the basic agent, except for how each move is scored. The
    basic agent scores a move by the number of steps remaining in its game,
    which mostly reflects when in the game the move was made (and how the
    rest of that game went) rather than how good the move was. This agent
    instead scores each move by the stability of the states that followed it,
    using knowledge of the game: how upright and still the pole is, and how
    centered the cart is.

    Flow:
    Generate a push direction given the current state of Cart-Pole while
    attempting to find similar situations from previous games where the
    stability that followed was the highest.

    Train only on games that did at least as well as the maximum average
    score, so that the model only trains on improving performances, assigning
    each move one of the following scores, as given by `scoring`:

    - "horizon" (default): the mean stability of the next `horizon` states,
      where states after the game was lost count as the failure stability.
    - "delta": the change in stability caused by the move.

    Unlike the basic agent's score, these do not depend on when in the game
    the move was made, nor on the game's step limit.
    """

    #: How each move is scored: "horizon" or "delta".
    scoring = 'horizon'
    #: The number of following states averaged by the "horizon" scoring.
    horizon = 15

    #: The pole angle (radians) and cart position at which the game is lost.
    angle_limit = 0.2095
    position_limit = 2.4
    #: The scale of the pole's angular velocity in the stability measure.
    angular_velocity_scale = 2.0
    #: The additional penalty applied to the state in which the game was lost.
    failure_penalty = 2.0

    def setup(self) -> None:
        """Setup the agent."""
        super().setup()
        self.max_avg_score = 0
        self.round_observations = []

    def stability(self, observation) -> float:
        """
        Return how stable a state is.

        0 is a centered cart with an upright, still pole; more negative values
        are less stable, with -1 roughly being the limits of the game.
        """
        cart_position, _, pole_angle, pole_angular_velocity = observation
        return -(abs(pole_angle) / self.angle_limit
                 + 0.5 * abs(pole_angular_velocity) / self.angular_velocity_scale
                 + 0.5 * abs(cart_position) / self.position_limit)

    def act(self, observation, round_num, step) -> int:
        """React to the observation to get the action."""
        if step == 1:
            self.round_observations = []
        self.round_observations.append([*observation])
        return super().act(observation, round_num, step)

    def move_scores(self, final_observation, failed: bool) -> list[float]:
        """
        Return the score of each move of the round.

        Parameters
        ----------
        final_observation : np.ndarray
            The observation after the last move of the round.
        failed : bool
            Whether the round ended by losing the game (rather than by
            reaching the game's step limit).
        """
        states = self.round_observations + [[*final_observation]]
        stability = np.array([self.stability(state) for state in states])
        failure_stability = stability[-1] - self.failure_penalty
        if failed:
            stability[-1] = failure_stability

        if self.scoring == 'delta':
            scores = stability[1:] - stability[:-1]
        elif self.scoring == 'horizon':
            scores = []
            for move in range(len(self.round_observations)):
                following = list(stability[move + 1:move + 1 + self.horizon])
                if failed:
                    following += [failure_stability] * (self.horizon - len(following))
                scores.append(np.mean(following))
        else:
            raise ValueError(f'Invalid scoring: {self.scoring}')
        return [float(score) for score in scores]

    def assign_reward(self, observation, scores, round_num, step) -> None:
        """Assign reward to model."""
        score = scores[-1]
        # avg of the last 100 games (or however many win_threshold is)
        avg_score = np.mean(scores[-self.win_threshold:])
        self.max_avg_score = max(self.max_avg_score, avg_score)

        # only train on games that did better than the current max avg score
        if score >= self.max_avg_score + 1:
            failed = score < self.env.spec.max_episode_steps
            self.trainee.train(
                features=self.goal_features,
                cases=[[move_score] for move_score in self.move_scores(observation, failed)],
                series=str(round_num),
            )
        else:
            self.trainee.remove_series_store()

        logger.info(
            'Round %s: score=%.0f high_score=%.0f avg_score=%.0f',
            round_num, score, np.max(scores), avg_score
        )
