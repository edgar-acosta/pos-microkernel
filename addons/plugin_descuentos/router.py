from fastapi import APIRouter

router = APIRouter()

@router.get("/apply")
async def apply_discount(total: float, rate: float):
    discount = total * (rate / 100)
    return {
        "status": "success",
        "original_price": total,
        "discount_applied": discount,
        "final_price": total - discount
    }