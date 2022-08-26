from fastapi import Depends
from fastapi_admin.depends import get_current_admin

from .resources import admin_app
from .routes import router

admin_app.include_router(router, dependencies=[Depends(get_current_admin)])
