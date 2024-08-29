import sys
import os

from utils.config_utils import get_config

config = get_config("bash")

def create_file(parent_dir: str = config["projects_dir"], filename: str = "foo.txt") -> str:
    return os.system(f"mkdir -p {parent_dir} && touch {parent_dir}/{filename}")

def delete_file(parent_dir: str = config["projects_dir"], filename: str = "foo.txt") -> str:
    return os.system(f"rm {parent_dir}/{filename}")

def create_project(type: str, project_name: str) -> str:
    # TODO: maybe clone the base files from a git repo
    return os.system(f"bash {os.path.dirname(__file__)}/scripts/new_{type}_project.sh {project_name}")

def create_git_repo(parent_dir: str = config["projects_dir"], repo_name: str = "foo") -> str:
    return os.system(f"git init {parent_dir}/{repo_name}")

def arbitrary_bash_command(command: str) -> str:
    if config["any_bash_command"]:
        return os.system(command)
    else:
        return "You don't have permission to run this command. The user can update this in the bash.json config file."


index = {
    "create_file": create_file,
    "delete_file": delete_file,
    "create_project": create_project,
    "arbitrary_bash_command": arbitrary_bash_command,
}
