import logging

from howso import engine
import pandas as pd
import numpy as np

from ...common.agent import BaseAgent

logger = logging.getLogger('howso.rl.examples.cart_pole')


class ValueLearningAgent(BaseAgent[np.ndarray, int]):
    """
    Cart-Pole value-learning agent.

    Utilizes only the original observation space as context features along with
    'score' to track rewards. Predicts the score for all possible actions in
    the action space for the given observation state and returns the push
    direction with the highest predicted score.

    This approach may be used if the action space is limited (i.e.,
    only a few possible moves, such as this game), low temporal complexity
    and a relatively simple score function.

    Flow:
    Select the push direction that maximizes the reward (score). Do this by
    first predicting the score for pushing left, then predicting the score for
    pushing right and selecting the direction that resulted in the highest
    score, and storing this action state.

    Train on played game, assigning cases a reward score from N to 1 based on
    on the number of steps in the game, thus the cases that were furthest from
    failure have higher scores than those immediately prior to failure. The
    score is capped to the max average score since all those cases are equally
    good with respect to temporal distance from failure.
    """

    def setup(self) -> None:
        """Setup the agent."""
        self.max_avg_score = 0

        # Setup Howso features
        self.features = {
            'score': {'type': 'continuous'},
            'push_direction': {
                # 0 = left
                # 1 = right
                'type': 'nominal',
                'data_type': 'number',
                'bounds': {
                    'allowed': [0, 1]
                }
            },
            'cart_position': {'type': 'continuous'},
            'cart_velocity': {'type': 'continuous'},
            'pole_angle': {'type': 'continuous'},
            'pole_angular_velocity': {'type': 'continuous'},
        }
        self.action_features = ['score']
        self.context_features = [
            'cart_position',
            'cart_velocity',
            'pole_angle',
            'pole_angular_velocity',
            'push_direction',
        ]

        self.trainee = engine.Trainee(features=self.features)
        self.trainee.set_auto_analyze_params(
            auto_analyze_enabled=True,
            analyze_threshold=1000,
        )
        if self.seed is not None:
            self.trainee.set_random_seed(self.seed)
        # Show all DataFrame columns
        pd.set_option('display.max_columns', None)

    def done(self, won=False):
        """Cleanup when finished."""
        self.trainee.delete()

    def act(self, observation, round_num, step) -> int:
        """React to the observation to get the action."""
        details = {}
        if self.explanation_level >= 2:
            details['influential_cases'] = True

        if self.explanation_level >= 3:
            details['feature_mda'] = True
            details['feature_residuals'] = True
            details['case_feature_residuals'] = True
            details['boundary_cases'] = 3

        # Find score if we push left by providing value for push in contexts
        react0 = self.trainee.react(
            contexts=[[*observation, 0]],
            context_features=self.context_features,
            action_features=self.action_features,
            details=details,
        )
        # Find score if we push right by providing value for push in contexts
        react1 = self.trainee.react(
            contexts=[[*observation, 1]],
            context_features=self.context_features,
            action_features=self.action_features,
            details=details,
        )
        action0 = react0['action']['score'][0]
        action1 = react1['action']['score'][0]
        target_action = None

        # None for score values may occur only when the model is empty
        # When no score found or scores are equal, randomly select action
        if action0 is None or action1 is None or action1 == action0:
            target_action = self.env.action_space.sample()
        else:
            # Select the push direction based on highest score
            target_action = 1 if action1 > action0 else 0

        # Log explanations for chosen action
        if target_action == 1:
            self.output_explanations(react1)
        else:
            self.output_explanations(react0)

        # Store result into series
        self.trainee.append_to_series_store(
            series=str(round_num),
            contexts=[[*observation, target_action]],
            context_features=self.context_features
        )

        return target_action

    def assign_reward(self, observation, scores, round_num, step) -> None:
        """Assign reward to model."""
        score = scores[-1]
        avg_score = np.mean(scores[-self.win_threshold:])
        self.max_avg_score = max(self.max_avg_score, avg_score)

        rewards = [
            # Cap reward as the average score
            [min(round(self.max_avg_score), score - i)]
            for i in range(step)
        ]

        self.trainee.train(
            features=self.action_features,
            cases=rewards,
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
            mda_data = react['explanation']['feature_mda'][0]
            if mda_data is not None:
                for feature in mda_data:
                    logger.info(
                        "Removing feature '%s' reduces accuracy of best action by: %s",
                        feature, mda_data[feature])

            # Get residuals
            residuals_data = react['explanation']['case_feature_residuals'][0]
            if residuals_data is not None:
                for feature in residuals_data:
                    logger.info(
                        "Feature %s has a residual of: %s",
                        feature, residuals_data[feature])

            residuals_data = react['explanation']['feature_residuals'][0]
            if residuals_data is not None:
                for feature in residuals_data:
                    logger.info(
                        "Feature %s has a residual of: %s",
                        feature, residuals_data[feature])
