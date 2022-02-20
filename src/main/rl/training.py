from pathlib import Path

from gym import register
from stable_baselines3 import PPO, TD3, A2C
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecMonitor

from src.main.rl.utils.constants import ALL_ACTION_WRAPPERS, ALL_OBSERVATION_WRAPPERS, ALL_SCENARIOS
from src.main.rl.utils.utils import WrapperMaker, parse_scenario_name, delete_env_id
from src.main.rl.wrapper.reward_wrapper2 import RewardOption2Wrapper
from src.main.rl.wrapper.reward_wrapper3 import RewardOption3Wrapper

num_cpu = 12
log_dir = "./model"


def train_agent(
    algorithm,
    environment,
    scenario_name: str,
    action_wrapper_name: str = None,
    obs_wrapper_name: str = None,
    reward_wrapper_name: str = None,
    name_ending: str = None,
):
    try:
        log_name_scenario = parse_scenario_name(scenario_name)
        log_name = f"{log_name_scenario}_{action_wrapper_name}_{obs_wrapper_name}_{algorithm.__name__}_{name_ending}"
        environment.reset()
        # From stable baselines / other work
        # n_steps=32, gae_lambda=0.8,batch_size=256,gamma=0.98,n_epochs=20,ent_coef=0.0, learning_rate=0.001, clip_range=0.2
        # Just some tires -> best one
        # n_steps=512, gae_lambda=0.8, batch_size=128, gamma=0.95, n_epochs=60,
        # ent_coef=0.0, learning_rate=0.0005, clip_range=0.2
        # This is used to use the same logic for model saving as for logs to directly identify them
        continue_search = True
        counter = 1
        model_save_path = ""
        while continue_search:
            my_file = Path(f"./models/{log_name_scenario}/{name_ending}/{log_name}_{counter}")
            if not my_file.is_dir():
                continue_search = False
                model_save_path = f"./models/{log_name_scenario}/{name_ending}/{log_name}_{counter}"
            counter += 1
        eval_callback = EvalCallback(environment, eval_freq=1000, best_model_save_path=model_save_path, verbose=1)
        model = algorithm("MlpPolicy",
            batch_size=16,
            n_steps=16,
            gamma=0.95,
            learning_rate= 1.74716807303931e-05,
            ent_coef= 0.04637566919041698,
            clip_range=0.2,
            n_epochs=10,
            gae_lambda=0.95,
            max_grad_norm= 5,
            vf_coef=0.6442556532729223,
            #net_arch="medium",
            #activation_fn="tanh",
            env=environment,
            verbose=1,
            tensorboard_log=f"./logs/{log_name_scenario}/{name_ending}/",
            device="cpu",
        ).learn(
            700000,
            tb_log_name=log_name,
            callback=eval_callback,
        )
    except Exception as exception:
        print("Error")
        print(exception)


def train_all_scenarios(
    scenarios: list,
    name_ending: str = None,
):
    # Algorithms
    algorithms = [PPO, ]#A2C, TD3]  # TD3]  # TD3 A2C
    for scenario in ALL_SCENARIOS[1:2]:
        parsed_scenario_name = parse_scenario_name(scenario)
        # With Wrappers
        #for action_wrapper in ALL_ACTION_WRAPPERS:
        #    for observation_wrapper in ALL_OBSERVATION_WRAPPERS:
#
        #        env_id = f"{parsed_scenario_name}_{observation_wrapper.__name__}_{action_wrapper.__name__}-v1"
        #        register(id=env_id, entry_point=scenario)
#
        #        # This is needed because make_vec_env does not allow a method with multiple parameters as wrapper_class
        #        wrapper_maker = WrapperMaker(action_wrapper, observation_wrapper)
        #        vec_env = make_vec_env(
        #            env_id, n_envs=num_cpu, wrapper_class=wrapper_maker.make_wrapper, monitor_dir=log_dir
        #        )
        #        vec_env_monitor = VecMonitor(vec_env)
        #        for alg in algorithms:
        #            train_agent(
        #                alg,
        #                vec_env_monitor,
        #                scenario,
        #                action_wrapper.__name__,
        #                observation_wrapper.__name__,
        #                name_ending,
        #            )
        #        delete_env_id(env_id)
        ## Single Wrapper
        #for action_wrapper in ALL_ACTION_WRAPPERS:
        #    env_id = f"{parsed_scenario_name}_None_{action_wrapper.__name__}-v1"
        #    register(id=env_id, entry_point=scenario)
        #    vec_env = make_vec_env(env_id, n_envs=num_cpu, wrapper_class=action_wrapper)
        #    vec_env_monitor = VecMonitor(vec_env)
        #    for alg in algorithms:
        #        train_agent(alg, vec_env_monitor, scenario, action_wrapper.__name__, None, name_ending)
        #        delete_env_id(env_id)
#
        #for observation_wrapper in ALL_OBSERVATION_WRAPPERS:
        #    env_id = f"{parsed_scenario_name}_{observation_wrapper.__name__}_None-v1"
        #    register(id=env_id, entry_point=scenario)
        #    vec_env = make_vec_env(env_id, n_envs=num_cpu, wrapper_class=observation_wrapper)
        #    vec_env_monitor = VecMonitor(vec_env)
        #    for alg in algorithms:
        #        train_agent(alg, vec_env_monitor, scenario, None, observation_wrapper.__name__, name_ending)
        #        delete_env_id(env_id)
        # Without Wrappers
        env_id = f"{parsed_scenario_name}_None_None-v1"
        register(id=env_id, entry_point=scenario)
        wrapper_maker = WrapperMaker(ALL_ACTION_WRAPPERS[1:2][0], ALL_OBSERVATION_WRAPPERS[3:4][0],RewardOption3Wrapper)
        vec_env = make_vec_env(
                    env_id, n_envs=num_cpu, wrapper_class=wrapper_maker.make_wrapper, monitor_dir=log_dir
                )
        vec_env_monitor = VecMonitor(vec_env)
        for alg in algorithms:
            train_agent(alg, vec_env_monitor, scenario, None, None,None, name_ending)
            delete_env_id(env_id)
