import logging

from howso import engine
import numpy as np
import pandas as pd

from ...common.agent import BaseAgent

logger = logging.getLogger('howso.rl.examples.cart_pole')


class BasicAgent(BaseAgent[np.ndarray, int]):
    """
    Cart-Pole basic agent.

    Utilizes only the original observation space as context features along
    with 'score' to track rewards. Predicts the push direction given the
    observation state and a desired score. The desired score is calculated
    as the maximum average score achieved plus one.

    This approach may be used if there is no or low temporal complexity and if
    the action space is simple.

    Flow:
    Generate a push direction given the current state of Cart-Pole while
    attempting to find similar situations from previous games where the score
    of those situations was similar to the max average score.

    Use a desired conviction of 5 instead of 1 to reduce exploratory decisions
    since similar previous cases were successful at lasting this long.

    Train on every played game, scoring each move by the discounted sum of the
    game's reward (1 per step) from that move on. Discounting makes a move's
    score mostly reflect the steps soon after it, rather than when in the game
    it was made or how the rest of the game went. When a game ends by reaching
    the step limit (rather than by being lost), the state it ended in counts
    as safe instead of worth nothing, since the pole was still up. Losing
    games are trained too, so that the model knows which situations and moves
    lead to losing.
    """

    #: The discount applied to each later step's reward when scoring a move.
    discount = 0.98

    def setup(self) -> None:
        """Setup the agent."""
        # Setup Howso features
        self.features = {
            # Action
            'push_direction': {
                # 0 = left
                # 1 = right
                'type': 'nominal',
                'data_type': 'number',
                'bounds': {'allowed': [0, 1], 'allow_null': False}
            },
            # Context
            'score': {'type': 'continuous'},
            'cart_position': {'type': 'continuous'},
            'cart_velocity': {'type': 'continuous'},
            'pole_angle': {'type': 'continuous'},
            'pole_angular_velocity': {'type': 'continuous'},
        }

        self.goal_features = ['score', ]
        self.action_features = ['push_direction', ]
        self.context_features = [
            'cart_position',
            'cart_velocity',
            'pole_angle',
            'pole_angular_velocity',
        ]

        self.trainee = engine.Trainee(features=self.features)
        self.trainee.set_auto_analyze_params(
            auto_analyze_enabled=True,
            context_features=self.context_features + self.action_features,
            # TODO 26254: Improve rebalance features for RL
            # rebalance_features=self.goal_features
        )
        self.goal_map = dict(zip(self.goal_features, [{"goal": "max"}]))

        if self.seed is not None:
            self.trainee.set_random_seed(self.seed)
        # Show all DataFrame columns
        pd.set_option('display.max_columns', None)

    def done(self, won=False) -> None:
        """Cleanup when finished."""
        self.trainee.delete()

    def act(self, observation, round_num, step) -> int:
        """React to the observation to get the action."""
        # TODO:22817 - lower conviction to 1
        desired_conviction = 3

        details = {}
        if self.explanation_level >= 2:
            details['influential_cases'] = True

        if self.explanation_level >= 3:
            details['feature_full_accuracy_contributions'] = True
            details['feature_full_residuals'] = True
            details['feature_full_residuals_for_case'] = True
            details['boundary_cases'] = 3

        react = self.trainee.react(
            desired_conviction=desired_conviction,
            contexts=[[*observation]],
            context_features=self.context_features,
            action_features=self.action_features,
            goal_features_map=self.goal_map,
            into_series_store=str(round_num),
            details=details,
        )
        push_direction = react['action']['push_direction'][0]

        self.output_explanations(react)

        return int(push_direction)

    def assign_reward(self, observation, scores, round_num, step) -> None:
        """Assign reward to model."""
        score = scores[-1]
        # avg of the last 100 games (or however many win_threshold is)
        avg_score = np.mean(scores[-self.win_threshold:])

        # the game was lost if it ended before the step limit, else it was cut off with the pole
        # still up, so count the state it ended in as safe: worth the most any state can be
        # (1 + discount + discount^2 + ... = 1 / (1 - discount))
        lost = score < self.env.spec.max_episode_steps
        value = 0.0 if lost else 1 / (1 - self.discount)

        # score each move by the discounted reward from it to the end of the game, last move first
        move_scores = []
        for _ in range(step):
            value = 1 + self.discount * value
            move_scores.append([value])
        move_scores.reverse()

        self.trainee.train(
            features=self.goal_features,
            cases=move_scores,
            series=str(round_num),
        )

        logger.info(
            'Round %s: score=%.0f high_score=%.0f avg_score=%.0f',
            round_num, score, np.max(scores), avg_score
        )

    def output_explanations(self, react) -> None:
        """
        Log react explanations based on explanation_level.

        Parameters
        ----------
        react : dict
            A react response.
        """
        if self.explanation_level >= 2:
            # Get influential cases
            influential_cases_data = react['explanation']['influential_cases']
            if influential_cases_data is not None:
                influential_cases_list = influential_cases_data[0]
                influential_cases = pd.DataFrame(influential_cases_list)
                logger.info("Most influential cases: \n%s", influential_cases)

        if self.explanation_level >= 3:
            # Get boundary cases
            boundary_cases_data = react['explanation']['boundary_cases']
            if boundary_cases_data is not None:
                boundary_cases_list = boundary_cases_data[0]
                boundary_cases = pd.DataFrame(boundary_cases_list)
                logger.info("Boundary cases: \n%s", boundary_cases)

            # Get mean decrease in accuracy
            ac_data = react['explanation']['feature_full_accuracy_contributions'][0]
            if ac_data is not None:
                for feature in ac_data:
                    logger.info(
                        "Removing feature '%s' reduces accuracy of best action by: %s",
                        feature, ac_data[feature])

            # Get residuals
            residuals_data = react['explanation']['feature_full_residuals_for_case'][0]
            if residuals_data is not None:
                for feature in residuals_data:
                    logger.info(
                        "Feature %s has a residual of: %s",
                        feature, residuals_data[feature])

            residuals_data = react['explanation']['feature_full_residuals'][0]
            if residuals_data is not None:
                for feature in residuals_data:
                    logger.info(
                        "Feature %s has a residual of: %s",
                        feature, residuals_data[feature])
