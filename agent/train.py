import time
from agent.q_learning_agent import QLearningAgent
from agent.traffic_env import TrafficEnv


def train(q_agent: QLearningAgent, environment: TrafficEnv, n_episodes: int=500, steps_per_episode: int=300):
    DECISION_TIMER = 60

    for episode in range(n_episodes):
        total_reward = 0
        environment.reset()

        for step in range(steps_per_episode):
            # Take action and learn only every DECISION_TIMER steps
            if step % DECISION_TIMER == 0:
                state = environment.get_state()
                action = q_agent.choose_action(state)
                environment.set_light_state(action)

                # Store for learning after environment updates
                learn_state = state
                learn_action = action

            # Update environment on *every* step
            environment.update()

            # Reward and learn logic still runs every DECISION_TIMER
            if step % DECISION_TIMER == 0:
                next_state = environment.get_state()
                reward = environment.compute_reward()
                total_reward += reward

                q_agent.learn(learn_state, learn_action, reward, next_state)

        print(f"Episode {episode+1}/{n_episodes} | Total Reward: {total_reward:.2f} | Epsilon: {q_agent.epsilon:.3f}")

    # Save after training
    q_agent.save("q_table.pkl")


if __name__ == '__main__':
    agent = QLearningAgent()
    # agent.load()
    env = TrafficEnv()
    train(agent, env, n_episodes=500)
