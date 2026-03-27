from io import BytesIO
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import require_admin
from ..models import Unit
from ..utils import get_unit_balance

router = APIRouter(prefix="/api/exports", tags=["exports"])

@router.get("/units.xlsx")
def export_units_excel(current_user=Depends(require_admin), db: Session = Depends(get_db)):
    units = db.query(Unit).filter(Unit.tenant_id == current_user.tenant_id).order_by(Unit.name.asc()).all()
    wb = Workbook(); ws = wb.active; ws.title = "Bakiye"
    ws.append(["Daire", "Sakin", "Toplam Borç", "Toplam Ödenen", "Kalan"])
    for unit in units:
        b = get_unit_balance(db, unit)
        ws.append([b["unit_name"], b["resident_name"] or "", float(b["total_debt"]), float(b["total_paid"]), float(b["balance"])])
    output = BytesIO(); wb.save(output); output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=unit-balances.xlsx"})

@router.get("/units.pdf")
def export_units_pdf(current_user=Depends(require_admin), db: Session = Depends(get_db)):
    units = db.query(Unit).filter(Unit.tenant_id == current_user.tenant_id).order_by(Unit.name.asc()).all()
    output = BytesIO(); pdf = canvas.Canvas(output, pagesize=A4); y = 800
    pdf.setFont("Helvetica", 12); pdf.drawString(50, y, "Daire Bakiye Raporu"); y -= 30
    for unit in units:
        b = get_unit_balance(db, unit)
        pdf.drawString(50, y, f"{b['unit_name']} | Borç: {b['total_debt']} | Ödenen: {b['total_paid']} | Kalan: {b['balance']}")
        y -= 20
        if y < 60:
            pdf.showPage(); y = 800
    pdf.save(); output.seek(0)
    return StreamingResponse(output, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=unit-balances.pdf"})
