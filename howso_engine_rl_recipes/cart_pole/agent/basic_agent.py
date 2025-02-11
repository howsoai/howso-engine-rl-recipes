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

    Train on played game, assigning cases a reward score from N to 1 based on
    on the number of steps in the game, thus the cases that were furthest from
    failure have higher scores than those immediately prior to failure. The
    score is capped to the max average score since all those cases are equally
    good with respect to temporal distance from failure.

    Additionally, only games that managed to achieve a score that's at least as
    good as the maximum average are trained, such that the model only trains on
    improving performances.
    """

    def setup(self) -> None:
        """Setup the agent."""
        self.max_avg_score = 0

        # Setup Howso features
        self.features = {
            # Action
            'push_direction': {
                # 0 = left
                # 1 = right
                'type': 'nominal',
                'data_type': 'number',
                'bounds': {'allowed': [0, 1]}
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
            context_features=self.context_features
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
        desired_conviction = 5

        details = {}
        if self.explanation_level >= 2:
            details['influential_cases'] = True

        if self.explanation_level >= 3:
            details['feature_mda_full'] = True
            details['feature_residuals_full'] = True
            details['case_feature_residuals_full'] = True
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
        self.max_avg_score = max(self.max_avg_score, avg_score)

        # assign each action a score, high to low, representing how many ticks before failure
        rewards = [
            [score - i]
            for i in range(step)
        ]

        # only train on games that did better than the current max avg score
        if score >= self.max_avg_score + 1:
            self.trainee.train(
                features=self.goal_features,
                cases=rewards,
                series=str(round_num),
            )
        else:
            self.trainee.remove_series_store()

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
            mda_data = react['explanation']['feature_mda_full'][0]
            if mda_data is not None:
                for feature in mda_data:
                    logger.info(
                        "Removing feature '%s' reduces accuracy of best action by: %s",
                        feature, mda_data[feature])

            # Get residuals
            residuals_data = react['explanation']['case_feature_residuals_full'][0]
            if residuals_data is not None:
                for feature in residuals_data:
                    logger.info(
                        "Feature %s has a residual of: %s",
                        feature, residuals_data[feature])

            residuals_data = react['explanation']['feature_residuals_full'][0]
            if residuals_data is not None:
                for feature in residuals_data:
                    logger.info(
                        "Feature %s has a residual of: %s",
                        feature, residuals_data[feature])
