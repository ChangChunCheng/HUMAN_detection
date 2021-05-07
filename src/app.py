from fastapi import FastAPI
from config import settings
import apis
from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


def create_app():
    if str(settings().MODE).upper() == 'DEVELOPMENT':
        app = FastAPI()
    else:
        app = FastAPI(docs_url='/docs', redoc_url='/redoc', openapi_url=None)
    return app


app = create_app()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", context={'request': request})


app.include_router(apis.Human.router, tags=['HumanDetection'])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings().HOST,
        port=settings().PORT,
        log_level="info"
    )
