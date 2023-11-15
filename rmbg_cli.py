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
        xdg_config_home = os.getenv("XDG_CONFIG_HOME")
        config = xdg_config_home and Path(xdg_config_home) / "rmbg.toml"
        home_config = Path.home() / ".rmbg.toml"

        if config and config.exists():
            return config
        elif home_config and home_config.exists():
            return home_config
        elif config:
            return config
        return home_config

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
        self._config["directory"] = str(value.absolute())
        with self._config_path.open("w") as f:
            toml.dump(self._config, f)

    @property
    def inputs_directory(self) -> Path:
        return self.directory / "inputs"

    @property
    def results_directory(self) -> Path:
        return self.directory / "results"

    @property
    def masks_directory(self) -> Path:
        return self.directory / "masks"


class Command(Enum):
    CONFIG = "config"
    INIT = "init"
    FOR = "for"


def create_parser(*, config: Config):
    parser = argparse.ArgumentParser(
        prog="rmbg",
        description="Automatically remove image backgrounds in seconds",
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # todo: create -g, --get option to show current config value for an option
    # + add choices
    config_cmd = subparsers.add_parser(
        Command.CONFIG.value,
        help="change configuration",
        description="Change configuration",
    )
    config_cmd.add_argument(
        "-d",
        "--directory",
        type=Path,
        help=f"path to a directory with images (default: {config.DEFAULT_DIRECTORY})",
    )

    subparsers.add_parser(
        Command.INIT.value,
        help="create the directory based on your configuration",
        description="Create the directory based on your configuration",
        epilog=f"According to your configuration it will create {config.directory}",
    )

    for_cmd = subparsers.add_parser(
        Command.FOR.value,
        help="remove background for an image",
        description="Remove background for an image",
    )
    for_cmd.add_argument(
        "image",
        help=(
            f"name of the image inside the {config.inputs_directory} directory to be "
            "processed (p.s. you can change the directory using the `config` command "
            "with the `--directory` option)"
        ),
    )

    return parser


class Args:
    def __init__(
        self,
        command: str | None,
        directory: Path | None = None,
        image: str | None = None,
    ) -> None:
        self.command = command and Command(command)
        self.directory = directory
        self.image = image


def process_args(args: Args, *, config: Config):
    match args.command:
        case Command.CONFIG:
            if args.directory:
                config.directory = args.directory
        case Command.INIT:
            config.directory.mkdir(parents=True, exist_ok=True)
            config.inputs_directory.mkdir(exist_ok=True)
            config.results_directory.mkdir(exist_ok=True)
            config.masks_directory.mkdir(exist_ok=True)
        case Command.FOR:
            if args.image:
                image_path = config.inputs_directory / args.image
                print(image_path)


def main():
    config = Config()
    parser = create_parser(config=config)
    args = Args(**vars(parser.parse_args()))
    process_args(args, config=config)


if __name__ == "__main__":
    main()
