from fnmatch import translate
from fastapi import FastAPI, HTTPException
from typing  import List, Optional
from db.task import tasks, Task

app = FastAPI()

# GET /tasks
@app.get(
        "/tasks", 
        response_model=List[Task], 
        summary="List all tasks", 
        description="Returns a list of all tasks."
)
def read_tasks():
    return tasks

# GET /tasks/:id
@app.get(
        "/tasks/{task_id}",
        response_model=Task,
        summary="Get task by ID"
)
def read_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(
        status_code=404, 
        detail="Task not found"
    )

# POST /tasks
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task


# PUT /tasks/{task_id}
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            # Update the existing task with the new values
            tasks[idx].title = updated_task.title
            tasks[idx].description = updated_task.description
            tasks[idx].completed = updated_task.completed
            return tasks[idx]  # Return the updated task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

# DELETE /tasks/{task_id}
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(idx)
            return task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)