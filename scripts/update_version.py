#!/usr/bin/env python
import re
import sys
from pathlib import Path

def update_version(init_file: str, new_version: str) -> None:
    """
    Update version in __init__.py file.
    
    Args:
        init_file: Path to __init__.py file
        new_version: New version string
    """
    init_file = Path(init_file)
    if not init_file.exists():
        print(f"Error: {init_file} does not exist")
        sys.exit(1)
        
    content = init_file.read_text()
    new_content = re.sub(
        r"__version__\s*=\s*['\"]([^'\"]+)['\"]",
        f'__version__ = "{new_version}"',
        content
    )
    
    if content == new_content:
        print(f"Warning: Version already set to {new_version}")
        return
        
    init_file.write_text(new_content)
    print(f"Updated version to {new_version}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <new_version>")
        print("Example: python update_version.py 2.7.3")
        sys.exit(1)
        
    new_version = sys.argv[1]
    if not re.match(r"^\d+\.\d+\.\d+$", new_version):
        print("Error: Version must be in format X.Y.Z")
        sys.exit(1)
        
    init_file = Path(__file__).parent.parent / "uzbekistan" / "__init__.py"
    update_version(init_file, new_version)

if __name__ == "__main__":
    main() 