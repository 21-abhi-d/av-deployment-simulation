# Fleet Management RL Simulation

## Overview
This project simulates a **fleet management system** using **Reinforcement Learning (RL)** in a **grid-based city environment**. A centralized RL agent controls a fleet of vehicles to efficiently pick up and drop off passengers.

## Features
✅ Custom **Gym Environment** (`FleetManagementEnv`) for vehicle routing.  
✅ Supports **PPO Algorithm** using Stable-Baselines3.  
✅ **Grid-based city simulation** (5x5, expandable).  
✅ Vehicles **avoid overlaps** and pick up passengers efficiently.  
✅ **Training and testing scripts** included.

---

## Installation
### **1. Install Dependencies**
```bash
pip install gym numpy stable-baselines3 matplotlib
```

---

## Running the Simulation
### **1. Train the RL Agent**
```bash
python train_agent.py
```
This script trains the RL agent using **Proximal Policy Optimization (PPO)** and saves the model as `fleet_manager_ppo.zip`.

### **2. Test the Trained Agent**
```bash
python test_agent.py
```
This script loads the trained model and simulates vehicle movements on the grid.

---

## Project Structure
```
📂 av-deployment-simulation
│── fleet_env.py       # Custom Gym environment
│── train_agent.py     # RL training script
│── test_agent.py      # RL model evaluation script
│── fleet_manager_ppo  # Trained model (after training)
│── README.md          # Documentation (this file)
```

---

## Environment Details
### **State Representation**
- A **5x5 grid** (expandable).
- 3D observation space:
  - **Red Channel (0)** → Vehicle positions.
  - **Green Channel (1)** → Passenger pickup locations.
  - **Blue Channel (2)** → Passenger destinations.

### **Action Space**
- `4 × num_vehicles` discrete actions:
  - Move **Up (0)**, **Down (1)**, **Left (2)**, **Right (3)**.

### **Reward Function**
- **+10** for picking up a passenger.
- **-1** penalty per step (to encourage efficiency).
- Future improvements: Penalizing long detours, rewarding faster drop-offs.

---

## Next Steps
📌 **Improve Reward Function** – Optimize for shorter travel times.  
📌 **Increase Grid Size** – Scale up to 10x10.  
📌 **Introduce Traffic Congestion** – Vehicles should slow down in crowded areas.  
📌 **Integrate SUMO** – Real-world traffic simulation (planned later).  

