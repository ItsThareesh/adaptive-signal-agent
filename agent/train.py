import time
from agent.q_learning_agent import QLearningAgent
from agent.traffic_env import TrafficEnv


def train(q_agent: QLearningAgent, environment: TrafficEnv, n_episodes: int=500, steps_per_episode: int=600):
    decision_timer = 90

    for episode in range(n_episodes):
        total_reward = 0

        # Initial decision
        learn_state = environment.get_state()
        learn_action = q_agent.choose_action(learn_state)
        environment.set_light_state(learn_action)

        # * Previously it was updating every 3 sec in a 20 sec game, which isn't ideal. So change it every game instead
        q_agent.epsilon = max(q_agent.epsilon * q_agent.epsilon_decay, q_agent.min_epsilon)

        for step in range(steps_per_episode):
            # Update Enviroment every Frame
            environment.update()

            # For every 90th step or 3 sec in a 30 FPS game
            if step % decision_timer == 0 and step > 0:
                # Learn from the previous decision
                reward = environment.compute_reward(learn_action)
                total_reward += reward
                # Get next state
                next_state = environment.get_state()

                q_agent.learn(learn_state, learn_action, reward, next_state)

                learn_state = next_state # Update Learn State for the next decision
                learn_action = q_agent.choose_action(learn_state) # Update Learn action for the next decision
                environment.set_light_state(learn_action) # Set lights for the next decision

        environment.reset()

        print(f"Episode {episode + 1}/{n_episodes} | Total Reward: {total_reward:.2f} | Epsilon: {q_agent.epsilon:.3f}")

        q_agent.save("q_table.pkl")


if __name__ == '__main__':
    agent = QLearningAgent()
    # agent.load()
    env = TrafficEnv()
    train(agent, env, n_episodes=500)
