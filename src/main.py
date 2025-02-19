from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Todo(BaseModel):
    id: int
    name: str
    completed: bool

# Mock database
todos = {
    1: Todo(id=1, name="Buy groceries", completed=False),
    2: Todo(id=2, name="Feed the cat", completed=True),
}

@app.get("/", response_model=List[Todo])
async def read_todos():
    return list(todos.values())

@app.get("/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    todo = todos.get(str(todo_id))
    # Print the todo variable
    print('read_todo', type(todo_id), todo_id, todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
    
@app.post("/", response_model=Todo)
async def create_todo(todo: Todo):
    todo_id = str(len(todos) + 1)
    todos[todo_id] = todo
    return todo

@app.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo: Todo):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id] = todo
    return todo

@app.delete("/{todo_id}", response_model=Todo)
async def delete_todo(todo_id: str):
    todo = todos.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return todo