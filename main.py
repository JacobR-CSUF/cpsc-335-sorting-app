"""
Main entry point for the Sorting Algorithm Visualizer
"""

import pygame
import sys
from app import SortingVisualizer

def main():
    """Main application loop"""
    visualizer = SortingVisualizer()
    running = True
    sort_generator = None
    last_step_time = 0

    while running:
        current_time = pygame.time.get_ticks()

        # Handle events
        for event in pygame.event.get():
            running, sort_generator = visualizer.event_handler.handle_events(event, sort_generator)
            if not running:
                break

        # Perform sorting step
        if visualizer.sorting and not visualizer.paused and sort_generator:
            if current_time - last_step_time > visualizer.speed:
                try:
                    next(sort_generator)
                    last_step_time = current_time
                except StopIteration:
                    sort_generator = None

        # Draw everything
        visualizer.draw()
        pygame.display.flip()
        visualizer.clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
