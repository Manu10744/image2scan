"""
 _                            ____
(_)_ __ ___   __ _  __ _  ___|___ \ ___  ___ __ _ _ __
| | '_ ` _ \ / _` |/ _` |/ _ \ __) / __|/ __/ _` | '_ \
| | | | | | | (_| | (_| |  __// __/\__ \ (_| (_| | | | |
|_|_| |_| |_|\__,_|\__, |\___|_____|___/\___\__,_|_| |_|
                   |___/
"""

import logging
import numpy as np
import imutils
import cv2

from ImageScanner import ImageScanner
from utils.argparsing import setup_argparser

logger = logging.getLogger("MAIN")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s | >>> %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    argparser = setup_argparser()
    args = argparser.parse_args()

    # Parsed arguments
    image = args.image
    destination = args.dest
    show_results = args.show_results

    logger.info("Image: {}".format(image))
    logger.info("Destination: {}".format(destination))
    logger.info("Showing Results: {}".format(show_results))

    if destination is not None:
        pass

    scanner = ImageScanner(image, show_results)
    scanner.scan()
