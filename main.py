from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Mock database
tasks_db = [
    {"id": 1, "title": "doing WADS project", "description": "Work on the Web Application Development project"},
    {"id": 2, "title": "eating", "description": "Have lunch"},
    {"id": 3, "title": "walking the dogs", "description": "Take the dogs for a walk in the park"}
]

class Task(BaseModel):
    id: int
    title: str
    description: str

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    tasks_db.append(task.dict())
    return task

@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task_by_id(task_id: int):
    """
    Get a task by its ID.
    """
    task = next((task for task in tasks_db if task["id"] == task_id), None)
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks/search/", response_model=List[Task])
async def search_tasks_by_name(name: str):
    """
    Search tasks by name.
    """
    found_tasks = [task for task in tasks_db if name.lower() in task["title"].lower()]
    if found_tasks:
        return found_tasks
    else:
        raise HTTPException(status_code=404, detail="No tasks found with the given name")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    """
    Update a task by its ID.
    """
    index = next((index for index, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if index is not None:
        tasks_db[index] = task.dict()
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """
    Delete a task by its ID.
    """
    index = next((index for index, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if index is not None:
        del tasks_db[index]
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")
