from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

def dual_response(request, template_name: str, context: dict):
    wants_html = "text/html" in request.headers.get("accept", "")
    if wants_html:
        return templates.TemplateResponse(template_name, {"request": request, **context})
    return JSONResponse(context)
