"""
Main Application Class for Sorting Algorithm Visualizer
"""
import sys

import pygame
import random
import time
from config import *
from ui_components import UIComponents
from event_handler import EventHandler

class SortingVisualizer:
    def __init__(self):
        pygame.init()

        # Window settings
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(APP_TITLE)

        # Initialize fonts
        self.fonts = {
            'title': pygame.font.Font(None, FONTS['TITLE_SIZE']),
            'medium': pygame.font.Font(None, FONTS['MEDIUM_SIZE']),
            'small': pygame.font.Font(None, FONTS['SMALL_SIZE']),
            'console': pygame.font.Font(pygame.font.match_font('monospace'), FONTS['CONSOLE_SIZE'])
        }

        # Initialize components
        self.ui = UIComponents(self.screen, self.fonts)
        self.event_handler = EventHandler(self)

        # Array settings
        self.array_size = SORTING_CONFIG['DEFAULT_ARRAY_SIZE']
        self.array = []
        self.sorting_array = []

        # Control variables
        self.sorting = False
        self.paused = False
        self.sorted = False
        self.started = False
        self.done_active = False
        self.speed = SORTING_CONFIG['DEFAULT_SPEED']
        self.current_indices = []
        self.console_messages = []
        self.max_console_lines = SORTING_CONFIG['MAX_CONSOLE_LINES']

        # Timing variables
        self.sort_start_time = 0
        self.pause_time = 0
        self.total_pause_duration = 0

        # Scroll variables
        self.array_scroll_offset = 0
        self.array_scroll_max = 0
        self.scrollbar_dragging = False
        self.scrollbar_rect = pygame.Rect(0, 0, 0, 0)

        # Initialize UI elements
        self._initialize_ui_elements()

        # Initialize data
        self.generate_array()

        # Input handling
        self.input_active = False
        self.input_text = str(self.array_size)

        # Clock
        self.clock = pygame.time.Clock()

    def _initialize_ui_elements(self):
        """Initialize all UI element positions"""
        # Input elements
        self.input_rect = pygame.Rect(60, 120, UI_DIMENSIONS['INPUT_WIDTH'],
                                      UI_DIMENSIONS['INPUT_HEIGHT'])
        self.array_display_rect = pygame.Rect(30, 170, self.width - 60,
                                             UI_DIMENSIONS['ARRAY_DISPLAY_HEIGHT'])
        self.array_content_rect = pygame.Rect(35, 175, self.width - 80, 50)

        # Algorithm selection
        self.selected_algorithm = "Bubble Sort"
        self.algorithm_buttons = self._create_algorithm_buttons()

        # Control buttons
        self._initialize_control_buttons()

        # Visualization panel
        self.viz_panel = pygame.Rect(30, 490, UI_DIMENSIONS['VIZ_PANEL_WIDTH'],
                                     UI_DIMENSIONS['VIZ_PANEL_HEIGHT'])

        # Console panel
        self.console_panel = pygame.Rect(450, 360, UI_DIMENSIONS['CONSOLE_WIDTH'],
                                        UI_DIMENSIONS['CONSOLE_HEIGHT'])

        # QUIT button
        self.quit_button = pygame.Rect((self.width - 120) // 2, 680, 120, 40)

    def _initialize_control_buttons(self):
        """Initialize control button positions (ABOVE visualization panel)"""
        btn_width = UI_DIMENSIONS['BUTTON_WIDTH']
        btn_height = UI_DIMENSIONS['BUTTON_HEIGHT']
        btn_spacing = UI_DIMENSIONS['BUTTON_SPACING']

        # Position buttons above the visualization panel
        btn_y = 420  # Positioned between algorithm selection and viz panel

        # Left-align buttons above the visualization panel
        start_x = 30  # Align with visualization panel

        self.start_button = pygame.Rect(start_x, btn_y, btn_width, btn_height)
        self.pause_button = pygame.Rect(start_x + btn_width + btn_spacing, btn_y, btn_width, btn_height)
        self.reset_button = pygame.Rect(start_x + (btn_width + btn_spacing) * 2, btn_y, btn_width, btn_height)

    def _create_algorithm_buttons(self):
        """Create algorithm button positions"""
        buttons = []
        start_x = 80
        start_y = 270
        cols = 3
        row_height = 40
        col_width = 180

        for i, algo in enumerate(ALGORITHMS):
            if algo:
                row = i // cols
                col = i % cols
                x = start_x + col * col_width
                y = start_y + row * row_height
                buttons.append({
                    'name': algo,
                    'rect': pygame.Rect(x - 15, y - 10, 160, 30),
                    'radio': pygame.Rect(x - 12, y - 7, 16, 16)
                })
        return buttons

    def generate_array(self):
        """Generate a random array for sorting"""
        self.array = [random.randint(SORTING_CONFIG['MIN_VALUE'],
                                    SORTING_CONFIG['MAX_VALUE'])
                     for _ in range(self.array_size)]
        self.sorting_array = self.array.copy()
        self.sorted = False
        self.sorting = False
        self.paused = False
        self.started = False
        self.current_indices = []
        self.console_messages = []
        self.array_scroll_offset = 0
        self.sort_start_time = 0
        self.total_pause_duration = 0

        # Display actual array
        algo_name = self.selected_algorithm.replace(" Sort", "")
        self.add_console_message(f"sortingapp$ running [{algo_name}] sort...")
        self.add_console_message(f"sortingapp$ utilizing array of size {self.array_size}")
        self.add_console_message(f"sortingapp$ Original array: {self.array}")

    def add_console_message(self, message):
        """Add a message to the console output"""
        self.console_messages.append(message)
        if len(self.console_messages) > self.max_console_lines:
            self.console_messages.pop(0)

    def start_sorting(self):
        """Start the sorting process and timer"""
        self.sort_start_time = time.time()
        self.total_pause_duration = 0
        self.done_active = False  # Reset DONE button when starting
        self.add_console_message(f"sortingapp$ visualizing...")

    def pause_sorting(self):
        """Pause the sorting and track pause time"""
        if not self.paused:
            self.pause_time = time.time()

    def resume_sorting(self):
        """Resume sorting and accumulate pause duration"""
        if self.paused:
            self.total_pause_duration += time.time() - self.pause_time

    def complete_sorting(self):
        """Calculate and display total sorting time"""
        if self.sort_start_time > 0:
            total_time = time.time() - self.sort_start_time - self.total_pause_duration
            algo_name = self.selected_algorithm.replace(" Sort", "")
            self.add_console_message(f"sortingapp$ [{algo_name}] sort took {total_time:.2f} seconds to complete")
            self.add_console_message(f"sortingapp$ Sorted array: {self.sorting_array}")
            self.add_console_message("sortingapp$ cleaning up...")

    def reset_sorting(self):
        """Reset the sorting state"""
        self.sorting_array = self.array.copy()
        self.sorting = False
        self.paused = False
        self.sorted = False
        self.started = False
        self.current_indices = []
        self.console_messages = []
        self.array_scroll_offset = 0
        self.sort_start_time = 0
        self.total_pause_duration = 0

        # Re-display initial messages with actual array
        algo_name = self.selected_algorithm.replace(" Sort", "")
        self.add_console_message(f"sortingapp$ running [{algo_name}] sort...")
        self.add_console_message(f"sortingapp$ utilizing array of size {self.array_size}")
        self.add_console_message(f"sortingapp$ Original array: {self.array}")

    def quit_application(self):
        """Quit the application"""
        pygame.quit()
        sys.exit()

    def draw(self):
        """Draw all UI components"""
        self.screen.fill(COLORS['BEIGE_BG'])

        self.ui.draw_header(self.width)
        self.ui.draw_input_section(self.input_rect, self.input_text, self.input_active)

        needs_scroll, scroll_max = self.ui.draw_array_display(
            self.array_display_rect, self.array_content_rect,
            self.sorting_array, self.array_scroll_offset, self.array_scroll_max
        )
        if needs_scroll:
            self.array_scroll_max = max(0, scroll_max)

        self.ui.draw_algorithm_selection(self.algorithm_buttons, self.selected_algorithm)
        self.ui.draw_control_buttons(self.start_button, self.pause_button,
                                    self.reset_button, self.started, self.paused)
        self.ui.draw_visualization_panel(self.viz_panel, self.sorting_array,
                                        self.current_indices, self.sorting, self.sorted)
        self.ui.draw_console_panel(self.console_panel, self.console_messages)
        self.ui.draw_quit_button(self.quit_button)
