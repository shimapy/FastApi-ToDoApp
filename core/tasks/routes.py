from typing import List
from fastapi import APIRouter,Path,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from tasks.models import TaskModel
from tasks.schemas import *
from core.database import get_db


# router = APIRouter(tags=['tasks'], prefix="/todo")
router = APIRouter(tags=['tasks'])

@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(
    completed: bool= Query(None, description="Filter tasks based on being completed or not"),
    limit: int= Query(10 ,gt=0, le=50, description="Limiting the number of items to retrieve"),
    offset: int =Query(0, ge=0, description="Use for paginating based on passed items"),
    db:Session=Depends(get_db)):
    query = db.query(TaskModel)
    if completed is not None:
        query = query.filter_by(is_compelete=completed)
    
    return query.limit(limit).offset(offset).all()

@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def retrieve_task_detail(task_id:int = Path(..., gt=0), db:Session=Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task_obj

@router.post("/tasks", response_model=TaskResponseSchema)
async def create_task(request:TaskCreateSchema, db:Session=Depends(get_db)):
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj

@router.put("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(request:TaskUpdateSchema,
                      task_id:int= Path(..., gt=0),
                      db:Session=Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    for field,value in request.model_dump(exclude_unset=True).items():
        setattr(task_obj, field, value)
        
    db.commit()
    db.refresh(task_obj)
    return task_obj
    
@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id:int= Path(..., gt=0), db:Session=Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    db.delete(task_obj)
    db.commit()
    # return JSONResponse(content="Task removed sucsessfuly.", status_code=200)
