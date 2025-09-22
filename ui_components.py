"""
UI Components for the Sorting Algorithm Visualizer
Contains all drawing methods for different UI sections
"""

import pygame
from config import COLORS, FONTS, UI_DIMENSIONS

class UIComponents:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts

    def wrap_text(self, text, font, max_width):
        """
        Wrap text to fit within the specified width
        Returns a list of text lines
        """
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            # Test if adding this word exceeds max width
            test_line = ' '.join(current_line + [word])
            text_width = font.size(test_line)[0]

            if text_width <= max_width:
                current_line.append(word)
            else:
                # Current line is full, start a new line
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Single word is too long, we need to break it
                    # This handles cases where a single word exceeds max_width
                    chars = list(word)
                    temp_word = ''
                    for char in chars:
                        if font.size(temp_word + char)[0] <= max_width:
                            temp_word += char
                        else:
                            if temp_word:
                                lines.append(temp_word)
                                temp_word = char
                    if temp_word:
                        current_line = [temp_word]

        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))

        return lines if lines else [text]  # Return original if no wrapping needed

    def draw_header(self, width):
        """Draw the header section"""
        header_rect = pygame.Rect(
            UI_DIMENSIONS['HEADER_MARGIN'],
            UI_DIMENSIONS['HEADER_MARGIN'],
            width - 2 * UI_DIMENSIONS['HEADER_MARGIN'],
            UI_DIMENSIONS['HEADER_HEIGHT']
        )
        pygame.draw.rect(self.screen, COLORS['BLUE_HEADER'], header_rect, border_radius=10)

        title = self.fonts['title'].render("Algorithm Sorting App", True, COLORS['WHITE'])
        title_rect = title.get_rect(center=(width // 2, 50))
        self.screen.blit(title, title_rect)

    def draw_input_section(self, input_rect, input_text, input_active):
        """Draw the array size input section"""
        # Question text
        question = self.fonts['medium'].render(
            "How elements will your array hold?", True, COLORS['BLACK']
        )
        self.screen.blit(question, (60, 90))

        # Input field
        pygame.draw.rect(self.screen, COLORS['WHITE'], input_rect)
        border_color = COLORS['BLACK'] if input_active else COLORS['GRAY']
        pygame.draw.rect(self.screen, border_color, input_rect, 2)

        # Input text
        text_surface = self.fonts['small'].render(input_text, True, COLORS['BLACK'])
        self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # "elements" label
        elements_text = self.fonts['small'].render("elements", True, COLORS['GRAY'])
        self.screen.blit(elements_text, (input_rect.x + input_rect.width + 10, input_rect.y + 5))

        # Randomize button
        pygame.draw.circle(self.screen, COLORS['BLUE_HEADER'], (235, 135), 8)
        pygame.draw.circle(self.screen, COLORS['WHITE'], (235, 135), 6)
        pygame.draw.circle(self.screen, COLORS['BLUE_HEADER'], (235, 135), 4)

        randomize_text = self.fonts['small'].render("Randomize", True, COLORS['BLACK'])
        self.screen.blit(randomize_text, (250, 125))

        return pygame.Rect(230, 120, 120, 30)  # Return randomize rect for click detection

    def draw_array_display(self, array_display_rect, array_content_rect,
                          sorting_array, array_scroll_offset, array_scroll_max):
        """Draw the array display with scrolling support"""
        # Draw main container
        pygame.draw.rect(self.screen, COLORS['WHITE'], array_display_rect, border_radius=5)
        pygame.draw.rect(self.screen, COLORS['GRAY'], array_display_rect, 2, border_radius=5)

        # Create array text
        array_str = str(sorting_array)
        text_surface = self.fonts['medium'].render(array_str, True, COLORS['BLACK'])
        text_width = text_surface.get_width()

        # Calculate if scrolling is needed
        available_width = array_content_rect.width - 20
        needs_scroll = text_width > available_width or len(sorting_array) > 30

        if needs_scroll:
            # Handle scrolling display
            self._draw_scrollable_array(
                array_display_rect, array_content_rect, text_surface,
                array_scroll_offset, array_scroll_max, available_width, text_width
            )
        else:
            # Center the text
            text_rect = text_surface.get_rect(center=array_display_rect.center)
            self.screen.blit(text_surface, text_rect)

        return needs_scroll, text_width - available_width if needs_scroll else 0

    def _draw_scrollable_array(self, display_rect, content_rect, text_surface,
                               scroll_offset, scroll_max, available_width, text_width):
        """Helper method to draw scrollable array content"""
        # Create clipping area
        self.screen.set_clip(content_rect)

        # Draw text with scroll offset
        text_x = content_rect.x - scroll_offset
        text_y = content_rect.centery - text_surface.get_height() // 2
        self.screen.blit(text_surface, (text_x, text_y))

        # Remove clipping
        self.screen.set_clip(None)

        # Draw scrollbar
        scrollbar_track = pygame.Rect(
            display_rect.right - 15,
            display_rect.y + 5,
            UI_DIMENSIONS['SCROLLBAR_WIDTH'],
            display_rect.height - 10
        )
        pygame.draw.rect(self.screen, COLORS['LIGHT_GRAY'], scrollbar_track, border_radius=5)

        # Draw scrollbar thumb if needed
        if scroll_max > 0:
            thumb_height = UI_DIMENSIONS['SCROLLBAR_HEIGHT']
            thumb_y_range = scrollbar_track.height - thumb_height
            thumb_y = scrollbar_track.y + int((scroll_offset / scroll_max) * thumb_y_range)

            thumb_rect = pygame.Rect(scrollbar_track.x, thumb_y,
                                    scrollbar_track.width, thumb_height)
            pygame.draw.rect(self.screen, COLORS['GRAY'], thumb_rect, border_radius=5)

    def draw_algorithm_selection(self, algorithm_buttons, selected_algorithm):
        """Draw algorithm radio buttons"""
        for algo_data in algorithm_buttons:
            # Draw radio button
            pygame.draw.circle(self.screen, COLORS['BLUE_HEADER'],
                             (algo_data['radio'].x + 8, algo_data['radio'].y + 8), 8)

            # Fill if selected
            if algo_data['name'] == selected_algorithm:
                pygame.draw.circle(self.screen, COLORS['WHITE'],
                                 (algo_data['radio'].x + 8, algo_data['radio'].y + 8), 4)
            else:
                pygame.draw.circle(self.screen, COLORS['WHITE'],
                                 (algo_data['radio'].x + 8, algo_data['radio'].y + 8), 6)

            # Algorithm name
            text = self.fonts['small'].render(algo_data['name'], True, COLORS['BLACK'])
            self.screen.blit(text, (algo_data['radio'].x + 25, algo_data['radio'].y))

    def draw_control_buttons(self, start_btn, pause_btn, reset_btn,
                           started, paused):
        """Draw control buttons with proper states"""
        # START button
        start_color = COLORS['DISABLED_GRAY'] if started else COLORS['GREEN']
        pygame.draw.rect(self.screen, start_color, start_btn, border_radius=5)
        start_text = self.fonts['medium'].render("START", True, COLORS['WHITE'])
        start_rect = start_text.get_rect(center=start_btn.center)
        self.screen.blit(start_text, start_rect)

        # PAUSE button
        pause_color = COLORS['ORANGE'] if started else COLORS['DISABLED_GRAY']
        pygame.draw.rect(self.screen, pause_color, pause_btn, border_radius=5)

        # Draw pause symbol
        bar_color = COLORS['RED'] if paused and started else COLORS['WHITE']
        self._draw_pause_symbol(pause_btn.center, bar_color)

        # RESET button
        reset_color = COLORS['RED'] if started else COLORS['DISABLED_GRAY']
        pygame.draw.rect(self.screen, reset_color, reset_btn, border_radius=5)
        reset_text = self.fonts['medium'].render("RESET", True, COLORS['WHITE'])
        reset_rect = reset_text.get_rect(center=reset_btn.center)
        self.screen.blit(reset_text, reset_rect)

    def _draw_pause_symbol(self, center, color):
        """Helper to draw pause symbol bars"""
        bar_width = 8
        bar_height = 20
        bar_spacing = 8

        pygame.draw.rect(self.screen, color,
                        (center[0] - bar_spacing - bar_width//2,
                         center[1] - bar_height//2, bar_width, bar_height))
        pygame.draw.rect(self.screen, color,
                        (center[0] + bar_spacing - bar_width//2,
                         center[1] - bar_height//2, bar_width, bar_height))

    def draw_visualization_panel(self, viz_panel, sorting_array, current_indices,
                                sorting, sorted_flag):
        """Draw the bar chart visualization panel"""
        pygame.draw.rect(self.screen, COLORS['GRAY'], viz_panel, border_radius=5)
        inner_rect = pygame.Rect(viz_panel.x + 5, viz_panel.y + 5,
                                viz_panel.width - 10, viz_panel.height - 10)
        pygame.draw.rect(self.screen, COLORS['WHITE'], inner_rect, border_radius=5)

        if len(sorting_array) == 0:
            return

        # Calculate and draw bars
        panel_width = viz_panel.width - 20
        panel_height = viz_panel.height - 20
        bar_width = panel_width // len(sorting_array) - 2
        max_value = max(sorting_array) if sorting_array else 1

        for i, value in enumerate(sorting_array):
            bar_height = int((value / max_value) * (panel_height - 10))
            x = viz_panel.x + 10 + i * (bar_width + 2)
            y = viz_panel.y + panel_height - bar_height

            # Determine color
            if i in current_indices and sorting:
                color = COLORS['RED']
            elif sorted_flag:
                color = COLORS['GREEN']
            else:
                color = COLORS['GREEN']

            pygame.draw.rect(self.screen, color, (x, y, bar_width, bar_height))

    def draw_console_panel(self, console_panel, console_messages, done_button):
        """Draw the console output panel with text wrapping"""
        pygame.draw.rect(self.screen, COLORS['CONSOLE_BG'], console_panel, border_radius=5)

        # Calculate available width for text (with padding)
        padding = 10
        max_text_width = console_panel.width - (padding * 2)

        # Process all messages and wrap them
        all_lines = []
        for message in console_messages:
            wrapped_lines = self.wrap_text(message, self.fonts['console'], max_text_width)
            all_lines.extend(wrapped_lines)

        # Calculate line height and max visible lines
        line_height = 18
        max_visible_lines = (console_panel.height - (padding * 2)) // line_height

        # Get the lines to display (most recent if there are too many)
        if len(all_lines) > max_visible_lines:
            display_lines = all_lines[-max_visible_lines:]
        else:
            display_lines = all_lines

        # Draw the wrapped lines
        y_offset = padding
        for line in display_lines:
            if y_offset + line_height > console_panel.height - padding:
                break  # Stop if we've reached the bottom

            text = self.fonts['console'].render(line, True, COLORS['CONSOLE_GREEN'])
            self.screen.blit(text, (console_panel.x + padding, console_panel.y + y_offset))
            y_offset += line_height

        # Draw DONE button
        pygame.draw.rect(self.screen, COLORS['DARK_GRAY'], done_button, border_radius=5)
        done_text = self.fonts['small'].render("DONE", True, COLORS['WHITE'])
        done_rect = done_text.get_rect(center=done_button.center)
        self.screen.blit(done_text, done_rect)
