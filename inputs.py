from typing import Optional

from fastapi_admin.widgets.inputs import Input


class InputWithMap(Input):
    input_type: Optional[str] = "text"
    template = "widgets/inputs/map.html"
