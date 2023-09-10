from abc import ABC, abstractmethod
import typing as t

import gymnasium as gym

ObsType = t.TypeVar("ObsType")
ActType = t.TypeVar("ActType")


class BaseAgent(ABC, t.Generic[ObsType, ActType]):
    """
    Base class for game agents.

    Defines interface for agents who play the game.

    Parameters
    ----------
    env : gym.Env
        The Gym environment.
    win_threshold : int
        The required threshold of rounds to solve the game.
    explanation_level : int
        The Howso react explanation level.
    seed: int, optional
        The agent seed.
    """

    def __init__(
        self,
        env: gym.Env,
        win_threshold: int,
        *,
        explanation_level: int = 1,
        seed: t.Optional[int] = None,
        **options: t.Dict
    ) -> None:
        self.env = env
        self.explanation_level = explanation_level
        self.seed = seed
        self.win_threshold = win_threshold
        self.options = options

    @abstractmethod
    def setup(self) -> None:
        """Setup the agent."""

    @abstractmethod
    def done(self, won: bool = False) -> None:
        """
        Close the agent and perform any cleanup.

        Parameters
        ----------
        won : bool
            If the game was won.
        """

    @abstractmethod
    def act(self, observation: ObsType, round_num: int, step: int) -> ActType:
        """
        React to the observation to get the action.

        Parameters
        ----------
        observation : ObsType
            The observation of the current step.
        round_num : int
            The current game round.
        step : int
            The game round's current step.

        Returns
        -------
        ActType
            The action to take in the game.
        """

    @abstractmethod
    def assign_reward(
        self,
        observation: ObsType,
        scores: t.Iterable[float],
        round_num: int,
        step: int
    ) -> None:
        """
        Assign reward to model.

        Parameters
        ----------
        observation : ObsType
            The observation from the final step.
        scores : list of float
            The final scores from all rounds.
        round_num : int
            The current game round.
        step : int
            The game round's current step.
        """
