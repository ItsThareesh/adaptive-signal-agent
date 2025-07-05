import os
import random
from collections import defaultdict
import pickle
import numpy as np
from utils.logger import logger


class QLearningAgent:
    def __init__(
        self,
        action_space=2,
        alpha=0.1,
        gamma=0.9,
        epsilon=1.0,
        min_epsilon=0.1,
        epsilon_decay=0.95,
    ):
        self.action_space = action_space
        self.q_table = defaultdict(lambda: np.zeros(action_space))

        # Hyperparameters
        self.alpha = alpha  # Learning Rate
        self.gamma = gamma  # Discount Factor
        self.epsilon = epsilon  # Exploration Rate
        self.min_epsilon = min_epsilon  # Min Exploration Rate upon decaying
        self.epsilon_decay = epsilon_decay  # Exploration Decay Rate

    def choose_action(self, state):
        """
        Chooses an action with probability epsilon to decide whether to explore or exploit
        """
        if random.random() < self.epsilon:
            return random.randint(0, self.action_space - 1)

        return np.argmax(self.q_table[state])

    def learn(self, state, action, reward, next_state):
        max_next_q = np.max(self.q_table[next_state])

        self.q_table[state][action] *= self.alpha
        self.q_table[state][action] += self.alpha * (reward + self.gamma * max_next_q)

    def save(self, epochs: int, path="q_table.pkl"):
        with open(path, "wb") as file:
            pickle.dump(
                {
                    "epochs": epochs,
                    "q_table": dict(self.q_table),
                    "epsilon": self.epsilon,
                },
                file,
            )

        logger.info("[+] Q-table saved to '%s'", path)

    def load(self, path="q_table.pkl"):
        if not os.path.exists(path):
            logger.error("[!] Q-table file '%s' not found.", path)
            logger.info("[!] Starting Game from 0 epochs.")
            return 0

        with open(path, "rb") as f:
            data = pickle.load(f)
            epoch = data["epochs"]
            self.q_table = defaultdict(
                lambda: np.zeros(self.action_space), data["q_table"]
            )
            self.epsilon = data.get("epsilon", self.epsilon)

        logger.info("[✓] Q-table loaded from '%s'", path)

        return epoch
