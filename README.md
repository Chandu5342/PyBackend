#  FastAPI Task Management API  
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

---

```
## 📁 Project Structure
├── main.py
├── models.py
├── schemas.py
├── storage.py  
└── README.md
```



## ▶️ Running the Server

### **1. Install dependencies**

pip install fastapi uvicorn pydantic 

2. Start the server
uvicorn main:app --reload


Server runs at:

http://127.0.0.1:8000


API docs:

http://127.0.0.1:8000/docs
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/78f85658-9b75-49a8-9c6f-7cbebc133235" />



📌 API Endpoints
1. Create Task
POST /tasks

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/5905cd87-3f7e-41cb-a502-bef55ac52477" />

2. Get All Tasks
GET /tasks
Filters:
/tasks?status=pending
/tasks?priority=high
/tasks?is_overdue=true

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/043747ea-9558-44b0-a427-431f49255cbd" />

3. Get Task by ID
GET /tasks/{id}
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/e8390ccf-faac-498f-931e-f11b95f6ac55" />


4. Update Task
PUT /tasks/{id}
Request:
{
  "title": "Buy groceries updated",
  "status": "completed"
}
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/9d2f74ef-b8cd-4e81-bc60-c34f8a925eaf" />

Business Rule:

If status becomes completed, set completed_at timestamp.

5. Delete Task
DELETE /tasks/{id}

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/8bf69e60-9b6e-4e7f-90a0-2f2b999daaef" />

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


✅ Conclusion

This FastAPI project demonstrates:

REST API design

Validation with Pydantic

Business rules handling

Clean folder structure

