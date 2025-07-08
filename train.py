from agent.q_learning_agent import QLearningAgent
from agent.traffic_env import TrafficEnv
from game.game_constants import GREEN_DURATION, YELLOW_DURATION
from ui.ui_constants import FPS
from utils.logger import logger


class TrainingParameters:
    def __init__(self):
        self.agent = QLearningAgent()
        self.environment = TrafficEnv()
        self.total_epochs = 100
        self.decisions_per_epoch = 15
        self.last_saved_epoch = self.agent.load()


def train(params: TrainingParameters, **kwargs):
    # Extract Argument Values
    last_epoch = params.last_saved_epoch
    verbose = kwargs.get("verbose", False)

    # Rendering Params
    render_game = kwargs.get("render_game", False)
    # If render game is True, then display epoch and decision count by default
    render_epoch = kwargs.get("render_epoch", render_game)
    render_decision = kwargs.get("render_decision", render_game)

    decision_timer = int((GREEN_DURATION + YELLOW_DURATION) * FPS)

    for epoch in range(params.total_epochs - params.last_saved_epoch):
        total_reward = 0
        decision_count = 1
        epoch_id = epoch + last_epoch + 1

        # Initial decision
        state = params.environment.get_state()
        action = params.agent.choose_action(state)
        params.environment.set_light_state(action)

        if verbose:
            logger.info("Epoch %d, Decision %d: %d", epoch_id, decision_count, action)

        for step in range(decision_timer * params.decisions_per_epoch):
            # Update Enviroment every Frame
            params.environment.update(
                render_game=render_game,
                epoch=epoch_id,
                render_epoch=render_epoch,
                decision=decision_count,
                render_decision=render_decision
            )

            if step % decision_timer == 0 and step > 0:
                # Learn from the previous decision
                reward = params.environment.compute_reward(action)
                total_reward += reward

                # Get next state
                next_state = params.environment.get_state()
                params.agent.learn(state, action, reward, next_state)

                # Agent makes the next decision
                next_action = params.agent.choose_action(next_state)
                params.environment.set_light_state(next_action)

                # Decision logging
                decision_count += 1

                if verbose:
                    logger.info("Epoch %d, Decision %d: %d", epoch_id, decision_count, action)

                # Update for next iteration
                state = next_state
                action = next_action

        params.environment.reset()

        logger.info(
            "Episode %d/%d | Total Reward: %.2f | Epsilon: %.3f",
            epoch + last_epoch + 1,
            params.total_epochs,
            total_reward,
            params.agent.epsilon
        )

        # Epsilon Decay
        params.agent.epsilon = max(
            params.agent.epsilon * params.agent.epsilon_decay,
            params.agent.min_epsilon,
        )

        params.agent.save(epoch_id)

    logger.info("[✓] Training Finished Successfully!!")


if __name__ == "__main__":
    train(TrainingParameters(), render_game=True, verbose=True)
