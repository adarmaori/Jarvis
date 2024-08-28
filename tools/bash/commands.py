import sys
import os

def create_file(parent_dir: str = ".", filename: str = "foo.txt") -> None:
    os.system(f"mkdir -p {parent_dir} && touch {parent_dir}/{filename}")

def delete_file(parent_dir: str = ".", filename: str = "foo.txt") -> None:
    os.system(f"rm {parent_dir}/{filename}")

if __name__ == "__main__":
    delete_file(filename="hello.txt")
