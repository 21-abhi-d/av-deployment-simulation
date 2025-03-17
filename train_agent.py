import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from fleet_env import FleetManagementEnv

# Create a vectorized environment
env = make_vec_env(FleetManagementEnv, n_envs=1)

# Initialize PPO agent
model = PPO("MlpPolicy", env, verbose=1)

# Train the agent
print("Training the RL agent...")
model.learn(total_timesteps=10000)

# Save the trained model
model.save("fleet_manager_ppo")
print("Training complete. Model saved as fleet_manager_ppo.")
