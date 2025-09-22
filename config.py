"""
Configuration file for the Sorting Algorithm Visualizer
Contains all colors, dimensions, and settings
"""

# Window Settings
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 740
APP_TITLE = "Algorithm Sorting App"

# Colors
COLORS = {
    'BEIGE_BG': (235, 205, 170),
    'BLUE_HEADER': (100, 149, 237),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GREEN': (50, 205, 50),
    'ORANGE': (255, 165, 0),
    'RED': (220, 20, 60),
    'GRAY': (192, 192, 192),
    'LIGHT_GRAY': (220, 220, 220),
    'DARK_GRAY': (64, 64, 64),
    'DISABLED_GRAY': (160, 160, 160),
    'CONSOLE_BG': (40, 40, 40),
    'CONSOLE_GREEN': (0, 255, 0),
}

# Font Sizes
FONTS = {
    'TITLE_SIZE': 36,
    'MEDIUM_SIZE': 24,
    'SMALL_SIZE': 20,
    'CONSOLE_SIZE': 14,
}

# UI Dimensions
UI_DIMENSIONS = {
    'HEADER_HEIGHT': 60,
    'HEADER_MARGIN': 20,
    'BUTTON_WIDTH': 120,
    'BUTTON_HEIGHT': 50,
    'BUTTON_SPACING': 25,
    'INPUT_WIDTH': 80,
    'INPUT_HEIGHT': 30,
    'ARRAY_DISPLAY_HEIGHT': 60,
    'VIZ_PANEL_WIDTH': 400,
    'VIZ_PANEL_HEIGHT': 180,
    'CONSOLE_WIDTH': 420,
    'CONSOLE_HEIGHT': 180,
    'SCROLLBAR_WIDTH': 10,
    'SCROLLBAR_HEIGHT': 20,
}

# Algorithm Names
ALGORITHMS = [
    "Bubble Sort", "Bucket Sort", "Counting Sort",
    "Heap Sort", "Insertion Sort", "Merge Sort",
    "Quick Sort", "Radix Sort", ""  # Empty for layout
]

# Sorting Settings
SORTING_CONFIG = {
    'DEFAULT_ARRAY_SIZE': 10,
    'MIN_ARRAY_SIZE': 5,
    'MAX_ARRAY_SIZE': 50,
    'MIN_VALUE': 10,
    'MAX_VALUE': 100,
    'DEFAULT_SPEED': 10,  # milliseconds
    'SCROLL_SPEED': 20,
    'MAX_CONSOLE_LINES': 8,
}
