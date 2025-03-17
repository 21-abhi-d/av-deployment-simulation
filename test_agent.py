from stable_baselines3 import PPO
from fleet_env import FleetManagementEnv

# Load the trained model
model = PPO.load("fleet_manager_ppo")

# Create the environment
env = FleetManagementEnv()
obs, _ = env.reset()

# Run the trained agent for 50 steps
for _ in range(50):
    action, _ = model.predict(obs)
    obs, reward, done, _, _ = env.step(action)
    
    # Render the environment
    env.render()

    if done:
        break

env.close()
