from fastapi import APIRouter, Request
from utils.responses import dual_response

router = APIRouter(prefix="/success", tags=["success"])


@router.get("/")
async def success_page(request: Request, session_id: str | None = None):
    context = {
        "title": "Pagamento completato",
        "session_id": session_id
    }

    return dual_response(
        request,
        template_name="success.html",
        context=context
    )
