import argparse, sys, logging
from sixsixutil import SixAiSix

logging.basicConfig(format="%(message)s")
logging.root.setLevel(logging.NOTSET)

sixsix = SixAiSix()

def wiggle_func(args):
    sixsix.wiggle()

def clk_func(args):
    sixsix.clk()

def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    wiggle = subparsers.add_parser("wiggle")
    wiggle.set_defaults(func=wiggle_func)

    clk = subparsers.add_parser("clk")
    clk.set_defaults(func=clk_func)

    return parser

def main():
    parser = get_parser()

    if (len(sys.argv) == 1):
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)
