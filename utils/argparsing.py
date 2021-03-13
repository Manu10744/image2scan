import argparse


def setup_argparser():
    parser = argparse.ArgumentParser(description="Convert images to scans using images from your local hard drive \
                                                  or the internet.")
    group = parser.add_argument_group("Arguments")
    group.add_argument("--image", required=True, metavar="<URL>", type=str,
                        help="The image you want to use. Can be a path to an image or, alternatively, a link to an " 
                             "image on the internet.")
    group.add_argument("--dest", required=False, metavar="<PATH>", type=str,
                        help="The directory you want the resulting scan to be stored in.")

    return parser