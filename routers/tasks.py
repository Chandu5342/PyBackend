from fastapi import APIRouter, HTTPException,Query
from datetime import datetime, date
import uuid

from schemas.task import TaskCreate, Task, TaskUpdate
from storage.db import tasksdb

router = APIRouter()


# ----------------------
#  CREATE TASK (POST)
# ----------------------
@router.post("/", response_model=Task)
def create_task(payload: TaskCreate):
    task_id = str(uuid.uuid4())
    now = datetime.utcnow()

   
    task = Task(
        id=task_id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        due_date=payload.due_date,
        created_at=now,
        updated_at=now,
        completed_at=None,
        is_overdue=False
    )

    # Save to in-memory DB
    tasksdb[task_id] = task

    return task

@router.get("/", response_model=list[Task])
def get_tasks(
    status: str | None = Query(None),
    priority: str | None = Query(None),
    is_overdue: bool | None = Query(None),
):
    result = []

    today = date.today()

    for task in tasksdb.values():
        task_dict = task.dict()

        # Determine overdue status 
        overdue = False
        if task.due_date and task.due_date < today and task.status != "completed":
            overdue = True

        task_dict["is_overdue"] = overdue

        
        if status and task.status != status:
            continue

        if priority and task.priority != priority:
            continue

        if is_overdue is not None and overdue != is_overdue:
            continue

        result.append(task_dict)

    return result
@router.get("/{task_id}", response_model=Task)
def get_task(task_id: str):
    if task_id not in tasksdb:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasksdb[task_id]
    task_dict = task.dict()

    # Overdue logic
    today = date.today()
    overdue = False
    if task.due_date and task.due_date < today and task.status != "completed":
        overdue = True

    task_dict["is_overdue"] = overdue

    return task_dict

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate):
    if task_id not in tasksdb:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasksdb[task_id]

    # Validate due_date
    if payload.due_date:
        today = date.today()
        if payload.due_date <= today:
            raise HTTPException(
                status_code=400,
                detail="due_date must be a future date"
            )

    # track old status
    old_status = task.status

    # Apply updates
    update_data = payload.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    # If status changed to completed → set completed_at
    if "status" in update_data:
        if update_data["status"] == "completed" and old_status != "completed":
            task.completed_at = datetime.utcnow()

    # Update timestamps
    task.updated_at = datetime.utcnow()

    # Save back to DB
    tasksdb[task_id] = task

    # Overdue logic
    overdue = False
    if task.due_date and task.due_date < date.today() and task.status != "completed":
        overdue = True

    task.is_overdue = overdue

    return task

@router.delete("/{task_id}")
def delete_task(task_id: str):
    if task_id not in tasksdb:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasksdb[task_id]

    # cannot delete tasks in progress
    if task.status == "in_progress":
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a task that is in progress"
        )

    # Delete task
    del tasksdb[task_id]

    return {"message": "Task deleted successfully"}