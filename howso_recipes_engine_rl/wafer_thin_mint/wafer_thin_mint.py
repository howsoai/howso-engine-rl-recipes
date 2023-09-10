from typing import Optional

import gymnasium as gym
from gymnasium import logger, spaces


class WaferThinMintEnv(gym.Env[int, int]):
    """
    An implementation of the wafer_thin_mint game where a player attempts to
    eat wafer-thin mints and avoid exploding.

    Based on the paper:
    Bontrager, Philip, Ahmed Khalifa, Damien Anderson, Matthew Stephenson,
    Christoph Salge, and Julian Togelius. '"Superstition" in the Network: Deep
    Reinforcement Learning Plays Deceptive Games.' In Proceedings of the
    AAAI Conference on Artificial Intelligence and Interactive Digital
    Entertainment, vol. 15, no. 1, pp. 10-16. 2019.
    https://www.aaai.org/ojs/index.php/AIIDE/article/download/5218/5074

    ## Action Space

        The action is an `integer` which can take values of `{0, 1}` indicating
        to eat another wafer or not.

        - 0: Don't eat
        - 1: Eat another wafer

    ## Observation Space

        The observation is an `integer` corresponding to the total wafers eaten.

    ## Rewards

        Since the goal is to keep from eating a maximum number wafers, a reward
        of `+1` for every wafer eaten is alloted unless the player "explodes"
        by eating wafers equal to the explosion threshold in which case a
        reward of -1 is alloted.

    ## Starting State

        The observation starts at 0.

    ## Episode End

        The episode ends if any one of the following occurs:

        1. Termination: The player stops eating.
        2. Termination: The player eats wafers equal to the explode threshold.
    """

    def __init__(self, render_mode: str, explode_threshold: int = 10):
        self.explode_threshold = explode_threshold
        self.steps_beyond_terminated = None
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Discrete(self.explode_threshold + 1)

    def step(self, action):
        err_msg = f"{action!r} ({type(action)}) invalid"
        assert self.action_space.contains(action), err_msg
        assert self.state is not None, "Call reset before using step method."

        # Eat another wafer
        if action == 1:
            self.state += 1

        exploded = self.state >= self.explode_threshold
        terminated = exploded or action == 0

        if not terminated:
            reward = 1
        elif self.steps_beyond_terminated is None:
            self.steps_beyond_terminated = 0
            if exploded:
                reward = -1
            else:
                reward = 0
        else:
            if self.steps_beyond_terminated == 0:
                logger.warn(
                    "You are calling 'step()' even though this "
                    "environment has already returned terminated = True. You "
                    "should always call 'reset()' once you receive 'terminated = "
                    "True' -- any further steps are undefined behavior."
                )
            self.steps_beyond_terminated += 1
            reward = 0

        return self.state, reward, terminated, False, {}

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        self.state = 0
        self.steps_beyond_terminated = None
        return self.state, {}
