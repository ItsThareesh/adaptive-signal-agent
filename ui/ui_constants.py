# PYGAME Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 3, 3
CELL_SIZE = WIDTH // COLS
CENTER: int = WIDTH//2
FPS = 30

# COLORS
CAR_COLORS = {
    'RED': (220, 20, 60),
    'YELLOW': (255, 215, 0),
    'ORANGE': (255, 140, 0),
    'BLUE': (30, 144, 255),
    'PURPLE': (138, 43, 226),
    'WHITE': (245, 245, 245)
}

UI_COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'GREY': (100, 100, 100),
    'GREEN': (30, 185, 30),
    'RED': (220, 20, 60),
}

# GRASS Properties
GRASS_BOX_SIZE = 225

# LANE Properties
LINE_WIDTH = 2
LINE_LENGTH = 200
LANE_WIDTH = WIDTH - 2 * GRASS_BOX_SIZE