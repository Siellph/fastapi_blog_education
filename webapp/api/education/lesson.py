from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.education.router import lesson_router
from webapp.crud.lesson import (
    create_lesson,
    delete_lesson,
    get_lesson_by_id,
    get_lessons_all_by_course_id,
    update_lesson,
)
from webapp.db.postgres import get_session
from webapp.schema.education.lesson import LessonCreate, LessonRead
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@lesson_router.post('/', response_model=LessonRead, tags=['Lessons'])
async def create_lesson_endpoint(
    course_id: int,
    lesson_data: LessonCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] == 'admin' or 'teacher':
        return await create_lesson(session=session, course_id=course_id, lesson_data=lesson_data)
    raise HTTPException(status_code=403, detail='Нет доступа для выполнения этой операции')


@lesson_router.get('/', response_model=List[LessonRead], tags=['Lessons'], response_class=ORJSONResponse)
async def get_all_lessons_by_course_endpoint(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    return await get_lessons_all_by_course_id(session=session, course_id=course_id)


@lesson_router.get('/{lesson_id}', response_model=LessonRead, tags=['Lessons'])
async def get_lesson_endpoint(
    course_id: int,
    lesson_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    lesson = await get_lesson_by_id(session=session, course_id=course_id, lesson_id=lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lesson not found')
    return lesson


@lesson_router.put('/{lesson_id}', response_model=LessonRead, tags=['Lessons'])
async def update_lesson_endpoint(
    course_id: int,
    lesson_id: int,
    lesson_data: LessonCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    updated_lesson = await update_lesson(
        session=session, course_id=course_id, lesson_id=lesson_id, lesson_data=lesson_data
    )
    if updated_lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lesson not found')
    return updated_lesson


@lesson_router.delete('/{lesson_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Lessons'])
async def delete_lesson_endpoint(
    course_id: int,
    lesson_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    try:
        return await delete_lesson(session=session, course_id=course_id, lesson_id=lesson_id)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lesson not found')
