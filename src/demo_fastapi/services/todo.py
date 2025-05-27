from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Sequence, Type

from demo_fastapi.schemas.todo import TodoCreate, TodoUpdate

from demo_fastapi.models.todo import Todo


class TodoService:
    @staticmethod
    async def get_todos(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Sequence[Todo]:
        """获取所有待办事项"""
        stmt = select(Todo).offset(skip).limit(limit)
        result = await db.execute(stmt)

        return result.scalars().all()

    @staticmethod
    async def get_todo_by_id(db: AsyncSession, todo_id: int) -> Optional[Todo]:
        """根据ID获取待办事项"""
        stmt = select(Todo).where(Todo.id == todo_id)
        return (await db.execute(stmt)).scalars().one_or_none()

    @staticmethod
    async def create_todo(db: AsyncSession, todo_data: TodoCreate) -> Todo:
        """创建待办事项"""
        db_todo = Todo()
        for key, value in todo_data.model_dump(exclude_unset=True).items():
            setattr(db_todo, key, value)
        db.add(db_todo)
        await db.commit()
        await db.refresh(db_todo)
        return db_todo

    @staticmethod
    async def update_todo(
        db: AsyncSession, todo_id: int, todo_data: TodoUpdate
    ) -> Optional[Todo]:
        """更新待办事项"""
        db_todo = await TodoService.get_todo_by_id(db, todo_id)
        if db_todo:
            # 仅更新提供的字段
            update_data = todo_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_todo, key, value)

            await db.commit()
            await db.refresh(db_todo)
        return db_todo

    @staticmethod
    async def delete_todo(db: AsyncSession, todo_id: int) -> bool:
        """删除待办事项"""
        db_todo = await TodoService.get_todo_by_id(db, todo_id)
        if db_todo:
            await db.delete(db_todo)
            await db.commit()
            return True
        return False
