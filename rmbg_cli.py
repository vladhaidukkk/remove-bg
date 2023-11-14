import argparse
import os
import tomllib
from pathlib import Path


class Config:
    @staticmethod
    def _get_config_path() -> Path:
        config_home = os.getenv("XDG_CONFIG_HOME")
        path = (
            Path(config_home) / "rmbg.toml"
            if config_home
            else Path.home() / ".rmbg.toml"
        )
        if not path.exists():
            path.open("x").close()
        return path

    @staticmethod
    def _get_config() -> dict:
        path = Config._get_config_path()
        with path.open("rb") as c:
            data = tomllib.load(c)
        return data


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
