from typing import Any

from flask_sqlalchemy.model import Model

HttpResponse = tuple[dict[str, Any] | Model, int]
