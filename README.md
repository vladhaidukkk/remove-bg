# Remove Bg CLI

The Remove Bg CLI tool is a powerful and efficient command-line utility designed to remove backgrounds from images seamlessly. It streamlines the process of isolating foreground objects by eliminating the background, providing users with clean, transparent images.

_It's based on [Rembg](https://github.com/danielgatis/rembg) open-source package._

## Installation

To install Remove Bg CLI, you will need to have Python and pip installed on your
system. Run this command:

```bash
pip install -i https://test.pypi.org/simple/ remove-bg
```

_It is important to note that this package is published on TestPyPI._

## Usage

Unlike most utilities, Remove Bg uses a different name for its executable script: `rmbg`. This is done for simplicity.

Remove Bg has three commands: `for`, `init` and `config`.

To remove background for an image, use `for` command:

```bash
rmbg for cat.png
```

If you want to have a directory where you will place all the images you want to process, use `init` command to initialize this directory:

```bash
rmbg init
```

With this directory, you can run `for` command with `--directory` parameter and it will search for images in it:

```bash
rmbg for --directory cat.png
```

By default, `init` command creates `remove-bg` directory in your home directory, but you can change this with the `config` command:

```bash
rmbg config --directory ~/dir/images
```

_Remove Bg CLI configuration can be found in `~/.config/rmbg.toml` or in `~/.rmbg.toml`._

If you want to get the value of a configuration parameter, use `config` command with `--get` option:

```bash
rmbg config --get directory
```

To see help, use the following command:

```bash
rmbg --help
```

You can also get help for a specific command:

```bash
rmbg for --help
```
