"""
Event Handler for the Sorting Algorithm Visualizer
Manages all user input and interactions
"""

import pygame
from config import SORTING_CONFIG

class EventHandler:
    def __init__(self, app):
        self.app = app

    def handle_events(self, event, sort_generator):
        """Main event handling dispatcher"""
        if event.type == pygame.QUIT:
            return False, sort_generator

        elif event.type == pygame.MOUSEWHEEL:
            return self._handle_mousewheel(event), sort_generator

        elif event.type == pygame.MOUSEBUTTONDOWN:
            return True, self._handle_mouse_down(event, sort_generator)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.app.scrollbar_dragging = False
            return True, sort_generator

        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)
            return True, sort_generator

        elif event.type == pygame.KEYDOWN:
            self._handle_keydown(event)
            return True, sort_generator

        return True, sort_generator

    def _handle_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if self.app.array_display_rect.collidepoint(pygame.mouse.get_pos()):
            self.app.array_scroll_offset -= event.y * SORTING_CONFIG['SCROLL_SPEED']
            self.app.array_scroll_offset = max(0, min(self.app.array_scroll_offset,
                                                      self.app.array_scroll_max))
        return True

    def _handle_mouse_down(self, event, sort_generator):
        """Handle mouse button down events"""
        # Check scrollbar
        if hasattr(self.app, 'scrollbar_rect') and self.app.scrollbar_rect.collidepoint(event.pos):
            self.app.scrollbar_dragging = True
            return sort_generator

        # Check DONE button
        if self.app.done_button.collidepoint(event.pos):
            self.app.handle_done_click()
            return None

        # Check input field
        if self.app.input_rect.collidepoint(event.pos):
            self.app.input_active = True
        else:
            self.app.input_active = False

        # Check randomize button
        randomize_rect = pygame.Rect(230, 120, 120, 30)
        if randomize_rect.collidepoint(event.pos):
            self.app.generate_array()
            return sort_generator

        # Check algorithm selection
        for algo_data in self.app.algorithm_buttons:
            if algo_data['rect'].collidepoint(event.pos):
                self.app.selected_algorithm = algo_data['name']
                # Update console when algorithm is changed
                if not self.app.started:
                    # Regenerate console messages with new algorithm name
                    self.app.console_messages = []
                    algo_name = self.app.selected_algorithm.replace(" Sort", "")
                    self.app.add_console_message(f"sortingapp$ running [{algo_name}] sort...")
                    self.app.add_console_message(f"sortingapp$ utilizing array of size {self.app.array_size}")
                    self.app.add_console_message(f"sortingapp$ Original array: {self.app.array}")

        # Check control buttons
        if self.app.start_button.collidepoint(event.pos):
            if not self.app.started and self.app.selected_algorithm == "Bubble Sort":
                self.app.sorting = True
                self.app.paused = False
                self.app.started = True
                self.app.start_sorting()  # Start the timer
                from sorting_visualizers import SortingVisualizers
                return SortingVisualizers.bubble_sort_visual(self.app.sorting_array, self.app)

        elif self.app.pause_button.collidepoint(event.pos):
            if self.app.started and self.app.sorting:
                if not self.app.paused:
                    self.app.pause_sorting()  # Track pause time
                    self.app.paused = True
                else:
                    self.app.resume_sorting()  # Resume and track duration
                    self.app.paused = False


        elif self.app.reset_button.collidepoint(event.pos):
            if self.app.started:
                self.app.reset_sorting()
                return None

        return sort_generator

    def _handle_mouse_motion(self, event):
        """Handle mouse motion for scrollbar dragging"""
        if self.app.scrollbar_dragging and self.app.array_scroll_max > 0:
            scrollbar_track = pygame.Rect(
                self.app.array_display_rect.right - 15,
                self.app.array_display_rect.y + 5,
                10,
                self.app.array_display_rect.height - 10
            )
            relative_y = event.pos[1] - scrollbar_track.y
            percentage = max(0, min(1, relative_y / scrollbar_track.height))
            self.app.array_scroll_offset = int(percentage * self.app.array_scroll_max)

    def _handle_keydown(self, event):
        """Handle keyboard input"""
        if self.app.input_active:
            if event.key == pygame.K_RETURN:
                try:
                    new_size = int(self.app.input_text)
                    if SORTING_CONFIG['MIN_ARRAY_SIZE'] <= new_size <= SORTING_CONFIG['MAX_ARRAY_SIZE']:
                        self.app.array_size = new_size
                        self.app.generate_array()
                except ValueError:
                    pass
                self.app.input_active = False
            elif event.key == pygame.K_BACKSPACE:
                self.app.input_text = self.app.input_text[:-1]
            else:
                if event.unicode.isdigit():
                    self.app.input_text += event.unicode

        # Arrow key scrolling
        elif self.app.array_display_rect.collidepoint(pygame.mouse.get_pos()):
            if event.key == pygame.K_LEFT:
                self.app.array_scroll_offset = max(0, self.app.array_scroll_offset - 20)
            elif event.key == pygame.K_RIGHT:
                self.app.array_scroll_offset = min(self.app.array_scroll_max, 
                                                  self.app.array_scroll_offset + 20)
