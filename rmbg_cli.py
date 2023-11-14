import argparse
import os
from enum import Enum
from pathlib import Path
from typing import TypedDict, cast

import toml


class ConfigDict(TypedDict):
    directory: str


class Config:
    DEFAULT_DIRECTORY = Path.home() / "remove-bg"

    def __init__(self) -> None:
        self._config_path = Config._get_config_path()
        if not self._config_path.exists():
            self._config_path.open("x").close()
        self._config = Config._parse_config(self._config_path)

    @staticmethod
    def _get_config_path() -> Path:
        config_home = os.getenv("XDG_CONFIG_HOME")
        return (
            Path(config_home) / "rmbg.toml"
            if config_home
            else Path.home() / ".rmbg.toml"
        )

    @staticmethod
    def _parse_config(path: Path) -> ConfigDict:
        with path.open() as f:
            data = toml.load(f)
        return cast(ConfigDict, data)

    @property
    def directory(self) -> Path:
        directory = self._config.get("directory")
        return Path(directory) if directory else Config.DEFAULT_DIRECTORY

    @directory.setter
    def directory(self, value: Path):
        self._config["directory"] = str(value)
        with self._config_path.open("w") as f:
            toml.dump(self._config, f)


class Command(Enum):
    CONFIG = "config"


def create_parser():
    parser = argparse.ArgumentParser(
        prog="rmbg",
        description="Automatically remove image backgrounds in seconds",
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    config = subparsers.add_parser(
        Command.CONFIG.value,
        help="change configuration",
        description="Change configuration",
    )
    config.add_argument(
        "-d",
        "--directory",
        type=Path,
        help=f"path to a directory with images (default: {Config.DEFAULT_DIRECTORY})",
    )

    return parser


class Args:
    def __init__(self, command: str | None, directory: Path | None = None) -> None:
        self.command = command and Command(command)
        self.directory = directory


def process_args(args: Args):
    config = Config()
    print(config.directory)

    match args.command:
        case Command.CONFIG:
            if args.directory:
                pass


def main():
    parser = create_parser()
    args = Args(**vars(parser.parse_args()))
    process_args(args)


if __name__ == "__main__":
    main()
