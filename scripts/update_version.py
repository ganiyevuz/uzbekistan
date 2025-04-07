#!/usr/bin/env python
import re
import sys
from pathlib import Path
import tomli
import tomli_w


def update_version(init_file: str, pyproject_file: str, new_version: str) -> None:
    """
    Update version in __init__.py and pyproject.toml files.

    Args:
        init_file: Path to __init__.py file
        pyproject_file: Path to pyproject.toml file
        new_version: New version string
    """
    # Update __init__.py
    init_file = Path(init_file)
    if not init_file.exists():
        print(f"Error: {init_file} does not exist")
        sys.exit(1)

    content = init_file.read_text()
    new_content = re.sub(
        r"__version__\s*=\s*['\"]([^'\"]+)['\"]",
        f'__version__ = "{new_version}"',
        content,
    )

    if content != new_content:
        init_file.write_text(new_content)
        print(f"Updated version to {new_version} in {init_file}")

    # Update pyproject.toml
    pyproject_file = Path(pyproject_file)
    if not pyproject_file.exists():
        print(f"Error: {pyproject_file} does not exist")
        sys.exit(1)

    with open(pyproject_file, "rb") as f:
        data = tomli.load(f)

    if data["tool"]["poetry"]["version"] != new_version:
        data["tool"]["poetry"]["version"] = new_version
        with open(pyproject_file, "wb") as f:
            tomli_w.dump(data, f)
        print(f"Updated version to {new_version} in {pyproject_file}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <new_version>")
        print("Example: python update_version.py 2.7.3")
        sys.exit(1)

    new_version = sys.argv[1]
    if not re.match(r"^\d+\.\d+\.\d+$", new_version):
        print("Error: Version must be in format X.Y.Z")
        sys.exit(1)

    project_root = Path(__file__).parent.parent
    init_file = project_root / "uzbekistan" / "__init__.py"
    pyproject_file = project_root / "pyproject.toml"

    update_version(init_file, pyproject_file, new_version)


if __name__ == "__main__":
    main()
