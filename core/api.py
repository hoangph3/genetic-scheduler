from typing import *
from threading import Thread, Event, Lock
from fastapi import FastAPI, Request, Body, Response
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
import uvicorn
import time
import os
import json

from core.scheduler import timetable


class DataModel(BaseModel):
    classrooms: List[dict] = [
        {
            "name": "6A",
            "subject": [
                {"name": "Toan", "instructor": "To01", "n_lessons": 4},
                {"name": "Ly", "instructor": "Ly01", "n_lessons": 3},
                {"name": "Hoa", "instructor": "Ho01", "n_lessons": 3},
                {"name": "Van", "instructor": "Va01", "n_lessons": 4},
                {"name": "Anh", "instructor": "An01", "n_lessons": 2},
                {"name": "Sinh", "instructor": "Si01", "n_lessons": 2},
                {"name": "Su", "instructor": "Su01", "n_lessons": 1},
                {"name": "Dia", "instructor": "Di01", "n_lessons": 1},
                {"name": "GDCD", "instructor": "GD01", "n_lessons": 1},
                {"name": "Tin", "instructor": "Ti01", "n_lessons": 2},
                {"name": "CN", "instructor": "To01", "n_lessons": 1},
                {"name": "The", "instructor": "Th01", "n_lessons": 2}
            ],
            "main_instructor": "To01"
        },
        {
            "name": "6B",
            "subject": [
                {"name": "Toan", "instructor": "To01", "n_lessons": 4},
                {"name": "Ly", "instructor": "Ly01", "n_lessons": 3},
                {"name": "Hoa", "instructor": "Ho01", "n_lessons": 3},
                {"name": "Van", "instructor": "Va01", "n_lessons": 4},
                {"name": "Anh", "instructor": "An01", "n_lessons": 2},
                {"name": "Sinh", "instructor": "Si01", "n_lessons": 2},
                {"name": "Su", "instructor": "Su01", "n_lessons": 1},
                {"name": "Dia", "instructor": "Di01", "n_lessons": 1},
                {"name": "GDCD", "instructor": "GD01", "n_lessons": 1},
                {"name": "Tin", "instructor": "Ti01", "n_lessons": 2},
                {"name": "CN", "instructor": "To01", "n_lessons": 1},
                {"name": "The", "instructor": "Th01", "n_lessons": 2}
            ],
            "main_instructor": "Ly01"
        },
        {
            "name": "6C",
            "subject": [
                {"name": "Toan", "instructor": "To01", "n_lessons": 4},
                {"name": "Ly", "instructor": "Ly01", "n_lessons": 3},
                {"name": "Hoa", "instructor": "Ho01", "n_lessons": 3},
                {"name": "Van", "instructor": "Va01", "n_lessons": 4},
                {"name": "Anh", "instructor": "An01", "n_lessons": 2},
                {"name": "Sinh", "instructor": "Si01", "n_lessons": 2},
                {"name": "Su", "instructor": "Su01", "n_lessons": 1},
                {"name": "Dia", "instructor": "Di01", "n_lessons": 1},
                {"name": "GDCD", "instructor": "GD01", "n_lessons": 1},
                {"name": "Tin", "instructor": "Ti01", "n_lessons": 2},
                {"name": "CN", "instructor": "To01", "n_lessons": 1},
                {"name": "The", "instructor": "Th01", "n_lessons": 2}
            ],
            "main_instructor": "Ho01"
        }
    ]


def run_app(api_host='0.0.0.0', api_port=8080, debug=True):
    app = FastAPI(docs_url=None, redoc_url=None, debug=debug)
    app.mount("/static", StaticFiles(directory="static"), name="static")


    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )


    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()


    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="/static/redoc.standalone.js",
        )


    @app.post("/schedule/generate")
    async def generate(data: DataModel):
        schedule_id = str(int(time.time()))
        path = os.path.join("logs", schedule_id)

        Thread(target=timetable, args=(path, data.classrooms)).start()

        content = {
            "message": "Generating schedule ...",
            "schedule_id": schedule_id
        }
        return JSONResponse(content=content, status_code=200)


    @app.get("/schedule/view/{schedule_id}")
    async def view(schedule_id: int):
        result = {}
        for schedule_file in sorted(Path(f"./logs/{schedule_id}").glob('*.json')):
            # load schedule
            with open(schedule_file) as f:
                schedule = json.load(f)
            classroom, n_conflicts = os.path.splitext(os.path.basename(schedule_file))[0].split('_')
            
            if classroom not in result:
                result[classroom] = {}
            result[classroom]['schedule'] = schedule
            result[classroom]['n_conflicts'] = int(n_conflicts)

        return JSONResponse(content=result, status_code=200)


    uvicorn.run(app, host=api_host, port=api_port)
