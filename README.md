# 🚦 Adaptive Traffic Signal Agent

A **Reinforcement Learning** powered Traffic Signal Agent that uses **Q-learning** to optimize traffic light phases in real-time, combined with an interactive **Pygame-based simulation**.

<p align="center">
  <video src="https://github.com/user-attachments/assets/eb94f783-6559-4df1-9f74-a764d0199233" />
</p>

## ✨ Key Features

- 🧠 **Q-learning Agent** with adaptive traffic light control and exploration/exploitation strategies
- ⚡ **Pre-trained Model** included (`q_table.pkl`) - **ready to run immediately!**
- 🔄 **Fully Trainable** - easily retrain with customizable hyperparameters
- 🎮 **Interactive GUI** with real-time visualization and traffic flow monitoring
- 🧱 **Modular Architecture** for easy experimentation and extension
- 📊 **Live Metrics** - FPS, car count, and remaining phase times

## 🚀 Quick Start

> [!IMPORTANT]
> **Prerequisites**: Ensure Python 3.8+ is installed and activate your virtual environment.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Demo (Pre-trained Agent)
```bash
python main.py
```
> 🎯 **Instant Demo**: Uses the pre-trained model for immediate results!

### 3. Train Your Own Agent *(Optional)*
```bash
python train.py
```
> **Customize**: Adjust training parameters in [`train.py`](./train.py)  
> **Auto-save**: Trained Q-table saved as [`q_table.pkl`](./q_table.pkl)

## 📁 Project Structure

```
traffic-rl/
├── LICENSE
├── README.md
├── main.py                 # Demo with pre-trained agent
├── train.py                # Train the Q-learning agent
├── q_table.pkl             # Pre-trained model (ready to use!)
├── requirements.txt        # Python dependencies
├── agent/                  # RL agent implementation
│   ├── __init__.py
│   ├── q_learning_agent.py # Q-learning algorithm
│   └── traffic_env.py      # Traffic simulation environment
├── game/                   # Core simulation logic
│   ├── __init__.py
│   ├── car.py              # Vehicle behavior & physics
│   ├── cars_controller.py  # Cars Controller according to traffic
│   ├── cars_spawner.py     # Dynamic car generation
│   ├── game_constants.py   # Game configuration constants
│   ├── lane_queue.py       # Lane-based vehicle queuing
│   ├── scheduler.py        # Smart traffic light scheduling
│   └── traffic_light.py    # Traffic light state machine
├── ui/                     # Visualization & rendering
│   ├── __init__.py
│   ├── renderer.py         # Pygame graphics engine
│   └── ui_constants.py     # UI configuration
└── utils/                  # Logging utilities
    ├── __init__.py
    └── logger.py
```

## 🧠 How It Works

### 🔍 **State Space**
The agent observes:
- **Cars waiting** in each direction (N, S, E, W)
- **Current light configuration**
- **Traffic flow patterns**

### ⚡ **Action Space**
- **Action 0**: North-South 🟢 GREEN, East-West 🔴 RED
- **Action 1**: East-West 🟢 GREEN, North-South 🔴 RED

### 🎯 **Smart Features**
- **Epsilon-greedy exploration** with decay
- **Green phase extension** for repeated actions (avoids unnecessary transitions)
- **Intersection safety** - waits for cars to clear before changing lights
- **Dynamic reward system** based on traffic efficiency

## ⚙️ Configuration

### Training Parameters
Edit [`train.py`](./train.py) to customize:
```python
alpha=0.25,           # Learning rate
gamma=0.9,            # Discount factor  
epsilon=1.0,          # Initial exploration rate
min_epsilon=0.1       # Minimum exploration rate  
epsilon_decay=0.955   # Exploration decay
```

### Agent Modes
- **Demo Mode**: `python main.py` (exploitation only)
- **Training Mode**: `python train.py` (exploration + learning)


## 🚀 Future Extensions

- 🧠 **Deep RL**: Upgrade to DQN with neural networks
- 🏙️ **Multi-Intersection**: Scale to city-wide traffic optimization
- 👥 **Multi-Agent**: Coordinate multiple intersections cooperatively

## 🎯 Highlights

| Feature | Status |
|---------|--------|
| ✅ Ready-to-run | Pre-trained model included |
| ✅ Scientific | Standard Q-learning implementation |
| ✅ Configurable | Easy hyperparameter tuning |
| ✅ Visual | Real-time traffic simulation |
| ✅ Modular | Clean, extensible architecture |
| ✅ Educational | Perfect for RL learning |

## 📈 Performance

- **Real-time**: 30 FPS smooth simulation
- **Efficiency**: Reduces average wait times by ~30% vs fixed timing

---

<br>

<div align="center">
<i>Built using Python, Pygame, and Reinforcement Learning</i>
</div>
