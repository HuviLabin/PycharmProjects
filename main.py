from fastapi import FastAPI, HTTPException, status
from schemas import UserRegister, UserRegisterResponse
from security import hash_password
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine, get_db

# יצירת הטבלאות במסד הנתונים (בפעם הראשונה)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")


# ---------- Users ----------
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)


# ---------- Projects ----------
@app.post("/projects", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project)


@app.get("/projects", response_model=list[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)


@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return crud.get_project(db, project_id)


# ---------- Tasks ----------
@app.post("/tasks", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return crud.get_task(db, task_id)


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.update_task(db, task_id, task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return crud.delete_task(db, task_id)

# "מסד נתונים" זמני בזיכרון לצורך תרגול הרישום
fake_users_db = []


@app.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    # בדיקה אם שם המשתמש כבר תפוס במערכת
    for existing_user in fake_users_db:
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

    # יצירת גיבוב (Hash) לסיסמה שהמשתמש שלח
    hashed_pwd = hash_password(user.password)

    # בניית רשומת המשתמש החדש (שימי לב: שומרים רק את ה-Hash, לעולם לא את הסיסמה המקורית!)
    new_user = {
        "id": len(fake_users_db) + 1,
        "username": user.username,
        "hashed_password": hashed_pwd
    }

    # שמירה במאגר הזמני
    fake_users_db.append(new_user)

    # הדפסה למסוף (טרמינל) כדי שנוכל לוודא בשלב הבא שהסיסמה אכן נשמרה מוצפנת
    print("Saved user in DB:", new_user)

    # החזרת המשתמש החדש (FastAPI יסנן החוצה את hashed_password בזכות response_model)
    return new_user