import logging

from howso import engine
import pandas as pd

from ...common.agent import BaseAgent

logger = logging.getLogger('howso.rl.examples.wafer_thin_mint')


class BasicAgent(BaseAgent[int, int]):
    """
    Wafer-Thin-Mint value-learning agent.

    Utilizes only the original observation space as context features along
    with 'score' to track rewards. Predicts the action to take given the
    observation state and a desired score. The desired score is calculated
    as the maximum score achieved plus one.

    This approach may be used if there is no or low temporal complexity and if
    the action space is simple.

    Flow:
    Generate an action given the current state of Wafer-Thin-Mint while
    attempting to find similar situations from previous games where the score
    of those situations was similar to the desired score.

    Train on played game, assigning all cases in the round the final reward of
    the round.
    """

    def setup(self) -> None:
        """Setup the agent."""
        self.features = {
            'wafer_count': {'type': 'ordinal', 'data_type': 'number'},
            'score': {'type': 'ordinal', 'data_type': 'number'},
            'action': {
                'type': 'nominal',
                'data_type': 'number',
                'bounds': {'allowed': [0, 1], 'allow_null': False}
            }
        }

        self.goal_features = ['score']
        self.context_features = ['wafer_count']
        self.action_features = ['action']
        self.goal_features_map = dict(zip(self.goal_features, [{"goal": "max"}]))

        self.trainee = engine.Trainee(features=self.features)
        self.trainee.set_auto_analyze_params(
            auto_analyze_enabled=True,
            context_features=self.context_features + self.action_features,
            rebalance_features=self.goal_features
        )
        if self.seed is not None:
            self.trainee.set_random_seed(self.seed)
        # Show all DataFrame columns
        pd.set_option('display.max_columns', None)

    def done(self, won=False) -> None:
        """Cleanup when finished."""
        self.trainee.delete()

    def act(self, observation, round_num, step) -> int:
        """React to the observation to get the action."""
        desired_conviction = 1.5

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
            contexts=[[observation]],
            context_features=self.context_features,
            action_features=self.action_features,
            goal_features_map=self.goal_features_map,
            into_series_store=str(round_num),
            details=details,
        )
        action = react['action']['action'][0]

        self.output_explanations(react)

        return int(action)

    def assign_reward(self, observation, scores, round_num, step) -> None:
        """Assign reward to model."""
        score = scores[-1]

        self.trainee.train(
            features=self.goal_features,
            cases=[[score]],
            series=str(round_num),
        )

        logger.info(
            'Round %s: score=%.0f', round_num, score)

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
