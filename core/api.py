from typing import *
from multiprocessing import Process
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import uvicorn
import time
import os
import json

from core.scheduler import timetable


class DataModel(BaseModel):
    classrooms: List[dict] = [
        {
            "name": "6A",
            "subjects": [
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
            "subjects": [
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
            "subjects": [
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
        },
        {
            "name": "7A",
            "subjects": [
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
            "main_instructor": "An01"
        },
        {
            "name": "7B",
            "subjects": [
                {"name": "Toan", "instructor": "To02", "n_lessons": 4},
                {"name": "Ly", "instructor": "Ly02", "n_lessons": 3},
                {"name": "Hoa", "instructor": "Ho02", "n_lessons": 3},
                {"name": "Van", "instructor": "Va02", "n_lessons": 4},
                {"name": "Anh", "instructor": "An02", "n_lessons": 2},
                {"name": "Sinh", "instructor": "Si02", "n_lessons": 2},
                {"name": "Su", "instructor": "Su01", "n_lessons": 1},
                {"name": "Dia", "instructor": "Di01", "n_lessons": 1},
                {"name": "GDCD", "instructor": "GD01", "n_lessons": 1},
                {"name": "Tin", "instructor": "Ti02", "n_lessons": 2},
                {"name": "CN", "instructor": "To02", "n_lessons": 1},
                {"name": "The", "instructor": "Th02", "n_lessons": 2}
            ],
            "main_instructor": "To02"
        },
        {
            "name": "7C",
            "subjects": [
                {"name": "Toan", "instructor": "To02", "n_lessons": 4},
                {"name": "Ly", "instructor": "Ly02", "n_lessons": 3},
                {"name": "Hoa", "instructor": "Ho02", "n_lessons": 3},
                {"name": "Van", "instructor": "Va02", "n_lessons": 4},
                {"name": "Anh", "instructor": "An02", "n_lessons": 2},
                {"name": "Sinh", "instructor": "Si02", "n_lessons": 2},
                {"name": "Su", "instructor": "Su01", "n_lessons": 1},
                {"name": "Dia", "instructor": "Di01", "n_lessons": 1},
                {"name": "GDCD", "instructor": "GD01", "n_lessons": 1},
                {"name": "Tin", "instructor": "Ti02", "n_lessons": 2},
                {"name": "CN", "instructor": "To02", "n_lessons": 1},
                {"name": "The", "instructor": "Th02", "n_lessons": 2}
            ],
            "main_instructor": "Ly02"
        }
    ]


def run_app(api_host='0.0.0.0', api_port=8080, debug=True):
    app = FastAPI(docs_url=None, redoc_url=None, debug=debug)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logs_dir = "./logs"


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
    async def generate_schedule(data: DataModel):
        schedule_id = int(time.time())
        path = os.path.join(logs_dir, str(schedule_id))

        Process(target=timetable, args=(path, data.classrooms)).start()

        content = {
            "message": "Generating schedule ...",
            "schedule_id": schedule_id
        }
        return JSONResponse(content=content, status_code=200)


    @app.get("/schedule/lists")
    async def lists_schedule():
        return JSONResponse(
            content={"schedule_id": list(map(int, sorted(os.listdir(logs_dir))))}, status_code=200
        )


    @app.delete("/schedule/view/{schedule_id}")
    async def delete_schedule(schedule_id: int):
        if not os.path.exists(os.path.join(logs_dir, str(schedule_id))):
            content = {
                "message": "Invalid schedule id",
                "schedule_id": schedule_id
            }
        else:
            os.system("rm -rf {}".format(os.path.join(logs_dir, str(schedule_id))))
            content = {
                "message": "Schedule has been deleted",
                "schedule_id": schedule_id
            }
        return JSONResponse(content=content, status_code=200)
        

    @app.get("/schedule/view/{schedule_id}")
    async def view_schedule(schedule_id: int):
        if not os.path.exists(os.path.join(logs_dir, str(schedule_id))):
            content = {
                "message": "Invalid schedule id",
                "schedule_id": schedule_id
            }
            return JSONResponse(content=content, status_code=200)
        result = {}
        for schedule_file in sorted(Path(os.path.join(logs_dir, str(schedule_id))).glob('*.json')):
            # load schedule
            with open(schedule_file) as f:
                schedule = json.load(f)
            classroom = os.path.splitext(os.path.basename(schedule_file))[0]
            result[classroom] = schedule

        return JSONResponse(content=result, status_code=200)


    @app.get("/schedule/download/{schedule_id}")
    async def download_schedule(schedule_id: int):
        if not os.path.exists(os.path.join(logs_dir, str(schedule_id))):
            content = {
                "message": "Invalid schedule id",
                "schedule_id": schedule_id
            }
            return JSONResponse(content=content, status_code=200)
        dfs = []
        for schedule_file in sorted(Path(os.path.join(logs_dir, str(schedule_id))).glob('*.json')):
            # load schedule
            with open(schedule_file) as f:
                schedule = json.load(f)
            classroom = os.path.splitext(os.path.basename(schedule_file))[0]
            df = pd.DataFrame(schedule)
            df['Room'] = classroom
            dfs.append(df)
        dfs = pd.concat(dfs)

        return StreamingResponse(
            iter([dfs.to_csv(index=False)]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={schedule_id}.csv"}
        )


    uvicorn.run(app, host=api_host, port=api_port)
