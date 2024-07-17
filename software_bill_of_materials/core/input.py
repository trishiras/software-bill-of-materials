import sys
from typing import List, Tuple
from argparse import ArgumentParser, Namespace


def parse_args() -> Tuple[Namespace, List[str]]:
    """Function that parses arguments from command line

    Returns:
        Tuple[Namespace, List[str]]: Known arguments will be passed
        passed in Namespace object while unknown will be passed in list
    """

    parser = ArgumentParser()

    parser.add_argument(
        "-t",
        "--target",
        dest="target",
        type=str,
        required=True,
        help="Give target as path/image to scan",
    )

    parser.add_argument(
        "-ov",
        "--output-via",
        dest="output_via",
        type=str,
        required=True,
        help="File or Webhook",
    )

    parser.add_argument(
        "-w",
        "--webhook",
        dest="webhook",
        type=str,
        default=None,
        help="Webhook URL",
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="output_file_path",
        type=str,
        default=None,
        help="File path to output results",
    )

    parser.add_argument(
        "-l",
        "--log",
        dest="loglevel",
        type=str,
        default="DEBUG",
        help="Log Level(DEBUG or ERROR )",
    )

    args, unknown = parser.parse_known_args()

    # Check if output_via is webhook and ensure webhook_url is provided
    if args.output_via == "webhook":
        if not args.webhook:
            parser.error("When output via webhook, webhook URL is necessary")
            sys.exit(1)

    # Check if output_via is file and ensure outfile_path is provided
    if args.output_via == "file":
        if not args.output_file_path:
            parser.error("When output via file, file details are necessary")
            sys.exit(1)

    return args, unknown
