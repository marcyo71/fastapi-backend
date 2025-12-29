from fastapi import APIRouter, Request
from utils.responses import dual_response

router = APIRouter(prefix="/cancel", tags=["cancel"])


@router.get("/")
async def cancel_page(request: Request):
    context = {
        "title": "Pagamento annullato"
    }

    return dual_response(
        request,
        template_name="cancel.html",
        context=context
    )
