from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from demo_fastapi.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from demo_fastapi.services.todo import TodoService

from demo_fastapi.core.deps import get_db_async

router = APIRouter()


@router.get("/", response_model=List[TodoResponse])
async def get_todos(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_async)
):
    """获取所有待办事项"""
    todos = await TodoService.get_todos(db, skip=skip, limit=limit)

    # todos = [TodoResponse.model_validate(todo) for todo in todos]

    return todos


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_db_async)):
    """根据ID获取待办事项"""
    todo = await TodoService.get_todo_by_id(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="待办事项未找到")
    return todo


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db_async)):
    """创建待办事项"""
    return await TodoService.create_todo(db, todo_data=todo)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int, todo: TodoUpdate, db: AsyncSession = Depends(get_db_async)
):
    """更新待办事项"""
    updated_todo = await TodoService.update_todo(db, todo_id=todo_id, todo_data=todo)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="待办事项未找到")
    return updated_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db_async)):
    """删除待办事项"""
    deleted = await TodoService.delete_todo(db, todo_id=todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="待办事项未找到")
    return None
