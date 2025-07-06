from agent.q_learning_agent import QLearningAgent
from agent.traffic_env import TrafficEnv
from game.game_constants import GREEN_DURATION, YELLOW_DURATION
from ui.ui_constants import FPS

import pygame


def main():
    agent = QLearningAgent(exploit=True)
    agent.load()  # Load the trained Q-table
    environment = TrafficEnv()
    running = True
    decision_timer = int((GREEN_DURATION + YELLOW_DURATION) * FPS)
    step = 0

    # Initial decision
    state = environment.get_state()
    action = agent.choose_action(state)
    environment.set_light_state(action)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Make a new decision every decision_timer steps
        if step % decision_timer == 0 and step > 0:
            state = environment.get_state()
            action = agent.choose_action(state)
            environment.set_light_state(action)

        # Update environment and render
        environment.update(render_game=True)
        step += 1

    pygame.quit()


if __name__ == "__main__":
    main()
