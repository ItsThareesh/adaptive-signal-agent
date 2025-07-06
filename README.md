# Adaptive Traffic Signal Agent

A Reinforcement Learning powered Traffic Signal Agent that uses Q-learning to optimize light phases in real-time combined with an interactive Pygame-based simulation.

https://github.com/user-attachments/assets/48e98ecc-e856-450f-80a4-f3f7a57b852e

## Features

- **Q-learning Agent** for adaptive traffic light control
- **Best-Performing Model** included (q_table.pkl) for immediate demo
- **Trainable**: Easily retrain or fine-tune the agent
- **GUI simulation** with Pygame for real-time visualization
- **Modular codebase** for easy experimentation

## Getting Started

Active the Python Development Environment in your current Terminal session.

1. Install Requirements
```bash
pip install -r requirements.txt
```
2. Run the Simulation (with Trained Agent)
```bash
python main.py
```  
3. Train the Agent
```bash
python train.py
```
- Training parameters can be adjusted in [train.py](./train.py) (total_epochs, etc).
- The trained Q-table is saved as [q_table.pkl](./q_table.pkl).

## Repository Structure

- `main.py`: Runs the simulation with the pretrained agent
  
- `train.py`: Trains the agent using Q-learning

- `q_table.pkl`: Serialized Q-table for reuse

- `game/`: Core simulation logic (Car spawning & stopping logic, Environment updates, Traffic Scheduler logic)

- `agent/`: Agent logic and utilities

- `ui/`: Visualization and Pygame rendering code

- `utils/`: Logging

## Usage Notes

- [main.py](./main.py) runs the simulation using the trained agent (exploitation only).
  
- [train.py](./train.py) will train the agent from scratch or continue from the last saved Q-table.
  
- The agent’s exploration/exploitation mode is controlled by the exploit parameter in QLearningAgent.

## Possible Extensions

- Replace Q-table with a deep neural network (DQN)

- Expand to multiple intersections or grid-based simulation

- Improve Model rewarding with average wait time
