import random


class Config:
    # Main loop
    LOOP_COUNT = 3001

    # Fishing loop. Change this value if WoW fishing ends earlier or later than fishing loop
    FISHING_LOOP = 50

    # Screen capture square from top left corner
    CAPTURE_X = 1400
    CAPTURE_Y = 200

    # How accurate template has to match in base_screenshot.png to be considered found
    TEMPLATE_RECOGNITION_THRESHOLD = 0.7

    # Threshold between frames which defies if there's fish. Lower - more sensitive
    # Check `diff` in logs for troubleshooting
    CATCH_THRESHOLD = 5

    # How many failures in a row will stop the script
    # This might happen if server restarts or you've been kicked
    MAX_FAILURES = 5

    # Cursor rest place (must not obstruct fishing float)
    # Coordinates from Top Left corner
    # Randomness is for more human like feeling. LOL
    @staticmethod
    def get_cursor_rest_place_x() -> int:
        return random.randint(1200, 1350)

    @staticmethod
    def get_cursor_rest_place_y() -> int:
        return random.randint(50, 150)
