from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from service.routers import router, get_apps, get_history
from settings import settings

services_router = APIRouter(prefix='')

services_router.include_router(router=router)
templates = Jinja2Templates(directory=f'{settings.APP_PATH}/templates/')


@services_router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    apps = await get_apps()
    history = await get_history()
    return templates.TemplateResponse('index.html', {
        'request': request,
        'apps': apps,
        'history': history,
    })
