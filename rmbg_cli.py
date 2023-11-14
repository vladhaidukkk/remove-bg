import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        prog="rmbg",
        description="Automatically remove image backgrounds in seconds",
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
