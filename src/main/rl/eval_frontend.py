import subprocess

import gym as gym
from py4j.java_gateway import JavaGateway
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_util import make_vec_env

from src.main.rl.utils.constants import ALL_SCENARIOS
from src.main.rl.utils.utils import WrapperMaker
from src.main.rl.wrapper.action_wrapper3 import ActionSpaceOption3Wrapper
from src.main.rl.wrapper.obs_wrapper5 import ObservationOption5Wrapper
from src.main.rl.wrapper.reward_wrapper3 import RewardOption3Wrapper


def eval_frontend(env):
    p = subprocess.Popen(["java", "-jar", "npp-java-adjusted-main.jar"])
    while True:
        try:
            gateway = JavaGateway(java_process=p)  # connect to the JVM
            entry = gateway.entry_point
            frontend = entry.getNPPUI()
            model = PPO.load("./models/scenario2/test_reward_2/scenario2_None_None_PPO_test_reward_2_69/best_model.zip")

            # model = A2C.load("./models/scenario2/test_reward_3/scenario2_None_None_A2C_test_reward_3_5/best_model.zip")
            score = []
            obs = env.reset()
            reward_total = 0
            counter=0
            for i in range(1000):
                action, _states = model.predict(obs, deterministic=True)
                moderator_setting = -1 if action[0][0] == 0 else 1

                wp1rpm_setting = -25 if action[0][1] == 0 else +25
                frontend.getSliderWP1RPM().setValue(frontend.getSliderWP1RPM().getValue() + wp1rpm_setting)
                frontend.getSliderRodPos().setValue(frontend.getSliderRodPos().getValue() + moderator_setting)
                frontend.getBCLWV1().doClick() if int(action[0][2]) == 0 else frontend.getBOpWV1().doClick()
                frontend.getBCLFV1().doClick() if int(action[0][3]) == 0 else frontend.getBOpFV1().doClick()
                cprpm_setting = -25 if action[0][4] == 0 else +25
                frontend.getSliderCPRPM().setValue(frontend.getSliderCPRPM().getValue() + cprpm_setting)
                frontend.timeStep()
                score.append(int(frontend.getPower()))
                # This is needed to get the same state for the environment. This is not the best way to do it.
                # Other option is to create a new env where only the fronend-calls are used, so we do not need
                # to do this here.
                obs, reward, done, info = env.step(action)
                reward_total += reward
                counter+=1
                if counter==239:
                    print("STOP")
                print(counter)
                if done:
                    print("Done")
                    break
            gateway.shutdown()
            p.kill()
            break
        except:
            pass


scenario = ALL_SCENARIOS[1:2][0]
env_dict = gym.envs.registration.registry.env_specs.copy()
env_id = "TestEnv-v1"
for env in env_dict:
    if env_id in env:
        del gym.envs.registration.registry.env_specs[env]

gym.register(id=env_id, entry_point=scenario)
x = WrapperMaker(ActionSpaceOption3Wrapper, ObservationOption5Wrapper, RewardOption3Wrapper)
vec_env = make_vec_env(env_id, n_envs=1, wrapper_class=x.make_wrapper)

eval_frontend(vec_env)
