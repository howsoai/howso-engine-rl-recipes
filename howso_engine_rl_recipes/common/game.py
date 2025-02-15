from abc import ABC, abstractmethod
from datetime import timedelta
import typing as t


import gymnasium as gym
from typing_extensions import NotRequired

from .agent import BaseAgent


class GameResult(t.TypedDict):
    """Type definition for game result."""
    win: bool
    rounds: int
    high_score: float
    total_cases: int
    duration: timedelta
    total_average_score: NotRequired[float]
    average_score: float


class BaseGame(ABC):
    """
    Base class to define the logic to play a game.

    Parameters
    ----------
    agent : type of BaseAgent
        The type of agent to use.
    explanation_level : int, default 1
        The react explanation level.
    max_rounds : int, default 2000
        The maximum games to attempt.
    render_mode : str
        The Gym render mode.
    seed : int
        The Gym and agent seed.
    """

    game_id = None

    def __init__(
        self,
        agent: t.Type[BaseAgent],
        *,
        explanation_level: int = 1,
        max_rounds: int = 1000,
        render_mode: t.Optional[str] = None,
        seed: t.Optional[int] = None
    ) -> None:
        self.seed = seed
        self.max_rounds = max_rounds
        self.explanation_level = explanation_level
        self.env = gym.make(self.game_id, render_mode=render_mode)
        self.agent_class = agent
        if seed is not None:
            self.env.action_space.seed(seed)

    def __enter__(self) -> "BaseGame":
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.close()

    def close(self) -> None:
        """Close the game and cleanup."""
        self.env.close()

    @abstractmethod
    def play(self) -> GameResult:
        """Play the game."""
