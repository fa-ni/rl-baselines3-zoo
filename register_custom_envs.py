from gym import register

def register_all_envs():
    register(id="Test_nik-v1", entry_point="src.main.rl.envs.scenario2:Scenario2")