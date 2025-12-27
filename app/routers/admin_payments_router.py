from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from app.services.payment_service import PaymentService
from app.utils.responses import dual_response   


router = APIRouter(prefix="/admin/payments", tags=["Admin Payments"])


@router.get("/", response_class=HTMLResponse)
async def list_payments(
    request: Request,
    method: str | None = Query(None),
    status: str | None = Query(None),
    format: str | None = Query(None)
):
    payments = PaymentService.list_payments(method=method, status=status)
    total = PaymentService.total_amount(method=method, status=status)

    context = {
        "payments": payments,
        "total": total,
        "filters": {"method": method, "status": status}
    }

    return dual_response(
        request=request,
        template_name="payments_list.html",
        context=context,
        json_data=context
    )

