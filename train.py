from agent.q_learning_agent import QLearningAgent
from agent.traffic_env import TrafficEnv
from game.game_constants import GREEN_DURATION, YELLOW_DURATION
from ui.ui_constants import FPS
from utils.logger import logger


class TrainingParameters:
    def __init__(self):
        self.q_agent = QLearningAgent()
        self.environment = TrafficEnv()
        self.total_epochs = 500
        self.frames_per_epoch = 600
        self.last_saved_epoch = self.q_agent.load()


def train(params: TrainingParameters, **kwargs):
    # Extract Argument Values
    last_epoch = params.last_saved_epoch
    verbose = kwargs.get("verbose", False)
    render_epoch = kwargs.get("render_epoch", False)

    decision_timer = int((GREEN_DURATION + YELLOW_DURATION) * FPS)

    for epoch in range(params.total_epochs-params.last_saved_epoch):
        total_reward = 0

        # Initial decision
        init_state = params.environment.get_state()
        init_action = params.q_agent.choose_action(init_state)
        params.environment.set_light_state(init_action)

        if verbose:
            logger.info(f"Agent made decision {init_action}")

        # Epsilon Decay
        params.q_agent.epsilon = max(
            params.q_agent.epsilon * params.q_agent.epsilon_decay,
            params.q_agent.min_epsilon
        )

        for step in range(params.frames_per_epoch):
            # Update Enviroment every Frame
            params.environment.update(epoch=epoch+last_epoch+1, render_epoch=render_epoch)

            if step % decision_timer == 0 and step > 0:
                # Learn from the previous decision
                reward = params.environment.compute_reward(init_action)
                total_reward += reward

                # Get next state
                next_state = params.environment.get_state()
                params.q_agent.learn(init_state, init_action, reward, next_state)

                # Agent makes the next decision
                next_action = params.q_agent.choose_action(next_state)
                params.environment.set_light_state(next_action)

                if verbose:
                    logger.info(f"Agent made decision {next_action}")

        params.environment.reset()

        print(
            f"Episode {epoch+last_epoch+1}/{params.total_epochs} | "
            f"Total Reward: {total_reward:.2f} | "
            f"Epsilon: {params.q_agent.epsilon:.3f}"
        )

        params.q_agent.save(epoch+last_epoch)

    print("Training Finished Successfully!!")


if __name__ == '__main__':
    train(TrainingParameters(), render_epoch=True)
