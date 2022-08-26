from fastapi import Depends
from fastapi_admin.depends import get_current_admin
from fastapi_admin.exceptions import (forbidden_error_exception,
                                      not_found_error_exception,
                                      server_error_exception,
                                      unauthorized_error_exception)
from starlette.status import (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND,
                              HTTP_500_INTERNAL_SERVER_ERROR)

from .resources import admin_app
from .routes import router

admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
admin_app.add_exception_handler(HTTP_401_UNAUTHORIZED, unauthorized_error_exception)
admin_app.include_router(router, dependencies=[Depends(get_current_admin)])
