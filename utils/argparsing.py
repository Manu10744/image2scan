import argparse
import os


def setup_argparser():
    parser = argparse.ArgumentParser(description="Convert images to scans using images from your local hard drive "
                                                 "or the internet.")

    group = parser.add_argument_group("Arguments")
    group.add_argument("--image", required=True, metavar="<URL>", type=str,
                       help="The image you want to use. Can be a path to an image or, alternatively, a link to an "
                            "image on the internet.")
    group.add_argument("--dest", default=os.path.join(os.getcwd(), "results"), metavar="<PATH>", type=str,
                       help="The directory you want the resulting scan to be stored in.")

    test_args = parser.add_argument_group("Arguments for Tests / Debugging")
    test_args.add_argument("--show-results", required=False, action="store_true",
                           help="If specified, the inidividual results of the image processing steps will be shown to "
                                "you in various GUI windows.")

    return parser
