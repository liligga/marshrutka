from fastapi import APIRouter, Depends
from fastapi_admin.depends import get_resources
from fastapi_admin.resources import Field, Link
from fastapi_admin.resources import Model as ModelResource
from fastapi_admin.template import templates
from fastapi_admin.widgets import displays
from starlette.requests import Request

router = APIRouter()


@router.get("/")
async def home(
    request: Request,
    resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "dashboard.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Dashboard",
            "page_pre_title": "overview",
            "page_title": "Dashboard",
        },
    )
