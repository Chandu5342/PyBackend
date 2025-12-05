# 📝 FastAPI Task Management API  
A simple Task Management REST API built using **FastAPI** with **in-memory storage**.  
This project was created as part of the backend assessment.

---

## 🚀 Features  
- Create, read, update, delete tasks  
- Filtering by status, priority, and overdue  
- Automatic timestamps (created_at, updated_at, completed_at)  
- Overdue task detection  
- Validation using Pydantic  
- In-memory storage (data clears on restart)  
- Basic unit tests using pytest  

---

## 📦 Tech Stack  
- **Python 3.10+**  
- **FastAPI**  
- **Uvicorn**  
- **Pydantic**  
- **Pytest**

---

## 📁 Project Structure
├── main.py
├── models.py
├── schemas.py
├── storage.py
├── utils.py
├── tests/
│ └── test_tasks.py
└── README.md


---

## ▶️ Running the Server

### **1. Install dependencies**
```sh
pip install fastapi uvicorn pydantic pytest

2. Start the server
uvicorn main:app --reload


Server runs at:

http://127.0.0.1:8000


API docs:

http://127.0.0.1:8000/docs

📌 API Endpoints
1. Create Task
POST /tasks
Request Body:
{
  "title": "Buy groceries",
  "description": "Milk, Bread",
  "status": "pending",
  "priority": "medium",
  "due_date": "2025-01-10T10:00:00"
}

Response:
201 Created

{
  "id": "uuid",
  "title": "Buy groceries",
  "description": "Milk, Bread",
  "status": "pending",
  "priority": "medium",
  "due_date": "2025-01-10T10:00:00",
  "created_at": "2025-12-04T10:00:00",
  "updated_at": "2025-12-04T10:00:00"
}

2. Get All Tasks
GET /tasks
Filters:
/tasks?status=pending
/tasks?priority=high
/tasks?is_overdue=true

Response Example:
[
  {
    "id": "uuid",
    "title": "Buy groceries",
    "status": "pending",
    "priority": "medium",
    "is_overdue": false
  }
]

3. Get Task by ID
GET /tasks/{id}
Response:
{
  "id": "uuid",
  "title": "Buy groceries",
  "status": "pending",
  "priority": "medium"
}

4. Update Task
PUT /tasks/{id}
Request:
{
  "title": "Buy groceries updated",
  "status": "completed"
}

Business Rule:

If status becomes completed, set completed_at timestamp.

5. Delete Task
DELETE /tasks/{id}
Business Rule:

❌ Tasks CANNOT be deleted if status = in_progress.

⚙️ Business Logic Summary
✔ Due Date Validation

Must be a future date

Else return 422 validation error

✔ Overdue Tasks

A task is overdue when:

due_date < now

status ≠ completed

Returned in response as:

"is_overdue": true

✔ Completed Tasks

When status changes → completed
→ Automatically set:

"completed_at": "<timestamp>"

🧪 Running Tests
Run all tests
pytest

Example test file: tests/test_tasks.py
def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test", "priority": "low"})
    assert response.status_code == 201

📘 Example cURL Commands
Create Task
curl -X POST "http://127.0.0.1:8000/tasks" \
-H "Content-Type: application/json" \
-d '{"title":"Test Task","priority":"medium"}'

List Tasks
curl "http://127.0.0.1:8000/tasks?status=pending"

Delete Task
curl -X DELETE "http://127.0.0.1:8000/tasks/<id>"

✅ Conclusion

This FastAPI project demonstrates:

REST API design

Validation with Pydantic

Business rules handling

Clean folder structure

Testing with pytest
