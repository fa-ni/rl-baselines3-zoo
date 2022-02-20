from src.main.rl.wrapper.action_wrapper2 import ActionSpaceOption2Wrapper
from src.main.rl.wrapper.action_wrapper3 import ActionSpaceOption3Wrapper
from src.main.rl.wrapper.obs_wrapper2 import ObservationOption2Wrapper
from src.main.rl.wrapper.obs_wrapper3 import ObservationOption3Wrapper
from src.main.rl.wrapper.obs_wrapper4 import ObservationOption4Wrapper
from src.main.rl.wrapper.obs_wrapper5 import ObservationOption5Wrapper

ALL_SCENARIOS = [
    "src.main.rl.envs.scenario1:Scenario1",
    "src.main.rl.envs.scenario2:Scenario2",
    "src.main.rl.envs.scenario3:Scenario3",
]
ALL_ACTION_WRAPPERS = [ActionSpaceOption2Wrapper, ActionSpaceOption3Wrapper]
ALL_OBSERVATION_WRAPPERS = [
    ObservationOption2Wrapper,
    ObservationOption3Wrapper,
    ObservationOption4Wrapper,
    ObservationOption5Wrapper,
]
