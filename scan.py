"""
 _                            ____
(_)_ __ ___   __ _  __ _  ___|___ \ ___  ___ __ _ _ __
| | '_ ` _ \ / _` |/ _` |/ _ \ __) / __|/ __/ _` | '_ \
| | | | | | | (_| | (_| |  __// __/\__ \ (_| (_| | | | |
|_|_| |_| |_|\__,_|\__, |\___|_____|___/\___\__,_|_| |_|
                   |___/
"""

import logging
import os

from ImageScanner import ImageScanner
from utils.argparsing import setup_argparser

logger = logging.getLogger("MAIN")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s | [%(levelname)s] %(message)s")
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

    if not os.path.exists(image):
        logger.error("The image on the given path could not be found! Please make sure the given file exists and its "
                     "path is correct.")
        raise SystemExit(1)

    if not os.path.exists(destination):
        logger.error("Cannot save the scan at the given destination path because it does not exist. "
                     "Please make sure to specify a path to an existing directory.")
        raise SystemExit(1)

    scanner = ImageScanner(image, destination, show_results)
    scanner.scan()
