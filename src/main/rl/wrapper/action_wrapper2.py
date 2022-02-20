import numpy as np
from gym import Wrapper
from gym.spaces import MultiBinary, Box, MultiDiscrete


class ActionSpaceOption2Wrapper(Wrapper):
    def __init__(self, env):
        super().__init__(
            env,
        )
        # Maybe we can check here which original value it had, if multibinary we go like this else.. TODO
        # 1. CR/Moderator Percent 2. WP1 RPM 3. WV1
        if type(env.action_space) == MultiBinary:
            self.action_space = MultiBinary(3)
        if type(env.action_space) == Box:
            self.action_space = Box(np.array([-1, -1, -1]).astype(np.float32), np.array([1, 1, 1]).astype(np.float32))
        if type(env.action_space) == MultiDiscrete:
            self.action_space = MultiDiscrete([3, 3, 3])
