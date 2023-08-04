import os
from datetime import datetime

import psutil as psutil
from fastapi import APIRouter
from sqlalchemy import select, insert, delete

from exceptions import Exceptions
from service.configs import App, History
from service.models import app_table, engine, history_table

router = APIRouter()


@router.get("/processes")
async def get_processes():
    processes = []
    for p in psutil.process_iter():
        processes.append({
            "pid": p.pid,
            "name": p.name(),
            "cpu_percent": p.cpu_percent(),
            "memory_percent": p.memory_percent(),
            "opened_at": datetime.fromtimestamp(p.create_time())
        })
    return processes


async def get_apps_from_db():
    try:
        statement = select(app_table)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(App.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        return Exceptions().get_exception(e)


@router.get("/apps/")
async def get_apps():
    try:
        process = await get_processes()
        await add_app(process)
        return process
    except Exception as e:
        return Exceptions().get_exception(e)


@router.post("/apps/")
async def add_app(request: list[App]):
    try:
        with engine.connect() as conn:
            conn.execute(
                insert(app_table),
                request)
            conn.commit()
        return "Posted"
    except Exception as e:
        return Exceptions().post_exception(e)


# Закрыть все приложения
@router.delete("/apps/all")
async def close_all():
    try:
        apps = await get_apps_from_db()
        for app in apps:
            del app["cpu_percent"]
            del app["memory_percent"]
            app["closed_at"] = datetime.now()
        delete_statement = delete(app_table)
        with engine.connect() as conn:
            conn.execute(
                insert(history_table),
                apps)
            conn.execute(delete_statement)
            conn.commit()
        for process in apps:
            pid = process.get('pid')
            os.system(f'taskkill /F /PID {pid}')
        return "All apps closed"
    except Exception as e:
        return Exceptions().delete_exception(e)


@router.get('/history/all')
async def get_history():
    try:
        statement = select(history_table)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(History.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        return Exceptions().get_exception(e)
