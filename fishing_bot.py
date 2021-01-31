import cv2
import time
import pyautogui
import numpy as np

from configs import Config
from loguru import logger
from PIL import ImageGrab


class Fish:

    catches = 0
    start_time = time.time()

    def main_loop(self):
        template = cv2.imread('fishing_float.png', 0)
        w, h = template.shape[::-1]

        for it in range(Config.LOOP_COUNT):
            self.display_stats(it)

            pyautogui.moveTo(Config.get_cursor_rest_place_x(), Config.get_cursor_rest_place_y(), duration=1)

            logger.info("1. Start fishing")

            # Start fishing by pressing 1 on the keyboard
            pyautogui.press('1')

            # Wait until fishing float appears on the screen
            time.sleep(2)

            logger.info("2. Fishing float is ready")

            # Capture game screenshot from top left corner + coordinates
            base_screen = ImageGrab.grab(bbox=(0, 0, Config.CAPTURE_X, Config.CAPTURE_Y))
            base_screen.save('base_screenshot.png')

            img_rgb = cv2.imread('base_screenshot.png')
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

            logger.info("3. Base screenshot is captured")

            # Compare template with screenshot and try to find it with 70% accuracy
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= Config.TEMPLATE_RECOGNITION_THRESHOLD)

            if not list(zip(*loc[::-1])):
                logger.error("Fishing float was not found. Restarting...")
                continue

            logger.info("4. Fishing float location found. Start fishing...")

            # Get position where fishing float has been found (from top left corner)
            x = list(zip(*loc[::-1]))[0][0]
            y = list(zip(*loc[::-1]))[0][1]

            # Magic loop (x, y - template's location on screen; w, h - template's width & height)
            self.fishing_loop(x, y, [0, ], w, h)

    # Loop for frame-by-frame comparison. Lasts 50 loops with 0.2s sleep.
    # This loop should last as long as fishing is happening on the screen
    def fishing_loop(self, x, y, average, w, h):
        for i in range(Config.FISHING_LOOP):
            # Sleep between frame checks (50 * 0.2s = 10s)

            # Once it's found, take another fishing float screenshot
            # This is required for comparison between frames - to recognize when it dips!
            clean_screen = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            mean = np.mean(clean_screen)

            # Get last element from `average` list and take `mean` out
            diff = average[-1] - mean
            logger.debug({"diff": diff})

            if diff >= Config.CATCH_THRESHOLD:
                logger.info({"CAUGHT!": diff})
                self.catches += 1
                self.click_mouse_at_loc(x, y)
                return
            average.append(mean)

            if i == Config.FISHING_LOOP - 1:
                logger.error("Nothing has been caught. Restarting...")

    @staticmethod
    def click_mouse_at_loc(x, y):
        pyautogui.moveTo(x, y, duration=0.3)
        pyautogui.mouseDown()
        time.sleep(0.2)
        pyautogui.mouseUp()

    def fetch_stats(self, it):
        fishing_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - self.start_time))
        catches_per_10min = self.catches * 600 / (time.time() - self.start_time)
        catches_per_10min = round(catches_per_10min * 100) / 100
        success_rate = 0 if it == 0 else round(self.catches * 100 / it)

        return fishing_time, catches_per_10min, success_rate

    def display_stats(self, it):
        fishing_time, catches_per_10min, success_rate = self.fetch_stats(it)

        logger.success('----------------------------------------------------------------------------')
        logger.success('   Fishing iteration: {0}/{1}    Fishing time: {2}    Catches: {3}'.format(it + 1, Config.LOOP_COUNT, fishing_time, self.catches))
        logger.success('                                                                            ')
        logger.success('          Catch rate: {0}/10min              Success rate: {1}%'.format(catches_per_10min, success_rate))
        logger.success('----------------------------------------------------------------------------')


# MONEEEEEYZ
f = Fish()
f.main_loop()
