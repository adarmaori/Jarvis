from pprint import pprint
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Due


with open("keys/todoist_api.key", "r") as f:
    key = f.read().strip()

api = TodoistAPI(key) 

def get_projects() -> list:
    try:
        projects = api.get_projects()
        return [project.__dict__ for project in projects]
    except Exception as error:
        print(error)
        return []


def get_project_id(name: str = 'Inbox') -> str:
    projects = get_projects()
    for project in projects:
        if project.name == name:
            return f"{project.id}"
    raise ValueError(f"Project {name} not found")


def add_task(
        task: str,
        project: str = 'Inbox',
        section: str = '/',
        parent: str = "",
        labels: list[str] | None = None,
        due_date: str | None = None,
        priority: int = 1
    ):
    # TODO: add some more parameters
    try:
        project_id = get_project_id(project)
        due = due_date if due_date else ""
        res = api.add_task(
            content=task, 
            project_id=project_id, 
            due_string=due, 
            priority=priority
        )
        return "Created task" if res else "Failed to create task"
    except Exception as error:
        print(error)        
        return "Failed to create task"


def get_tasks_project(project: str = 'Inbox') -> list:
    try:
        project_id = get_project_id(project)
        tasks = api.get_tasks(project_id)
        return [task.__dict__ for task in tasks]
    except Exception as error:
        print(error)
        return []


def get_all_tasks() -> list:
    try:
        tasks = api.get_tasks()
        return [task.__dict__ for task in tasks]
    except Exception as error:
        print(error)
        return []


def get_tasks_by_due_date(due_date: str) -> list:
    tasks = get_all_tasks()
    return [task for task in tasks if task.due_date == due_date]


index = {
    "add_task": add_task,
    "get_projects": get_projects,
    "get_tasks_project": get_tasks_project,
    "get_all_tasks": get_all_tasks,
}


print(Due(string="2024-08-01", is_recurring=False, date=None).to_dict())