import gym
import numpy as np
from gym import spaces
import random

class FleetManagementEnv(gym.Env):
    """A simple city grid environment for fleet management"""
    def __init__(self, grid_size=5, num_vehicles=2, num_passengers=3):
        super(FleetManagementEnv, self).__init__()
        
        self.grid_size = grid_size
        self.num_vehicles = num_vehicles
        self.num_passengers = num_passengers
        
        # State: Vehicle positions + Passenger pickup/destination locations
        self.state = None
        
        # Action space: Move vehicles (Up, Down, Left, Right) or Assign vehicle to request
        self.action_space = spaces.Discrete(4 * num_vehicles)
        
        # Observation space: Grid representation (vehicles + passengers)
        self.observation_space = spaces.Box(low=0, high=1, shape=(grid_size, grid_size, 3), dtype=np.float32)
        
        self.reset()

    def reset(self, seed=None, options=None):
        """Resets the environment to a new state"""
        super().reset(seed=seed)  # Gym 0.26+ requires calling super().reset(seed)

        self.vehicles = [self._random_position() for _ in range(self.num_vehicles)]
        self.passengers = [(self._random_position(), self._random_position()) for _ in range(self.num_passengers)]
        self.steps = 0

        obs = self._get_observation()
        info = {}  # Gym 0.26+ requires returning an additional info dictionary
        return obs, info

    def step(self, action):
        """Takes a step in the environment"""
        vehicle_index = action // 4
        move = action % 4

        if vehicle_index < self.num_vehicles:
            self._move_vehicle(vehicle_index, move)

        # Reward based on pickups
        reward = self._calculate_reward()

        # Check if all passengers have been picked up
        done = len(self.passengers) == 0
        truncated = False  # Gym 0.26+ requires a "truncated" flag

        return self._get_observation(), reward, done, truncated, {}

    def _random_position(self):
        """Returns a random position within the grid"""
        return (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))

    def _move_vehicle(self, vehicle_index, move):
        """Moves a vehicle in the given direction while preventing overlaps."""
        x, y = self.vehicles[vehicle_index]
        new_x, new_y = x, y  # Store potential new position

        if move == 0 and y > 0:  # Up
            new_y -= 1
        elif move == 1 and y < self.grid_size - 1:  # Down
            new_y += 1
        elif move == 2 and x > 0:  # Left
            new_x -= 1
        elif move == 3 and x < self.grid_size - 1:  # Right
            new_x += 1

        if (new_x, new_y) not in self.vehicles:
            self.vehicles[vehicle_index] = (new_x, new_y)

    def _calculate_reward(self):
        """Calculates the reward for the step"""
        reward = 0
        for i, (pickup, dropoff) in enumerate(self.passengers):
            for v in self.vehicles:
                if v == pickup:
                    reward += 10  # Reward for picking up a passenger
                    self.passengers.pop(i)  # Remove passenger from list
                    break
        return reward - 1  # Small penalty for each step to encourage efficiency

    def _get_observation(self):
        """Returns the current state representation"""
        obs = np.zeros((self.grid_size, self.grid_size, 3))
        for v in self.vehicles:
            obs[v[1], v[0], 0] = 1  # Mark vehicle positions in red channel
        for pickup, dropoff in self.passengers:
            obs[pickup[1], pickup[0], 1] = 1  # Mark passenger locations in green channel
            obs[dropoff[1], dropoff[0], 2] = 1  # Mark destinations in blue channel
        return obs

    def render(self):
        """Prints the grid state for debugging"""
        grid = np.zeros((self.grid_size, self.grid_size), dtype=str)
        grid[:] = '.'
        for v in self.vehicles:
            grid[v[1], v[0]] = 'V'
        for pickup, _ in self.passengers:
            grid[pickup[1], pickup[0]] = 'P'
        print("\n".join([" ".join(row) for row in grid]))
        print("\n")

# Test environment
if __name__ == "__main__":
    env = FleetManagementEnv()
    env.reset()
    env.render()
    for _ in range(10):
        action = env.action_space.sample()
        obs, reward, done, _ = env.step(action)
        env.render()
        if done:
            break