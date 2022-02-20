import numpy as np
from gym import Wrapper
from gym.spaces import MultiBinary, Box, MultiDiscrete


class ActionSpaceOption3Wrapper(Wrapper):
    def __init__(self, env):
        super().__init__(env)
        # 1. CR/Moderator Percent 2. WP1 RPM 3. WV1 4. SV1 5. CP RPM
        if type(env.action_space) == MultiBinary:
            self.action_space = MultiBinary(5)
        if type(env.action_space) == Box:
            self.action_space = Box(
                np.array([-1, -1, -1, -1, -1]).astype(np.float32), np.array([1, 1, 1, 1, 1]).astype(np.float32)
            )
        if type(env.action_space) == MultiDiscrete:
            self.action_space = MultiDiscrete([3, 3, 3, 3, 3])
