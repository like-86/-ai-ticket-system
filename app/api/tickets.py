from fastapi  import APIRouter
from app.db.database import SessionLocal
from app.db.models import Ticket

router = APIRouter(prefix="/api/tickets", tags=["tickets"])

@router.get("")
def list_tickets():
    db = SessionLocal()
    tickets = db.query(Ticket).order_by(Ticket.id.desc()).all()
    db.close()
    return [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "priority": t.priority,
            "created_at": str(t.created_at),
        }
        for t in tickets
    ]
@router.get("/{ticket_id}")
def read_ticket(ticket_id: int):
    db = SessionLocal()
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    db.close()
    if not ticket:
        return{"error": "Ticket not found"}
    return {
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority,
        "created_at": str(ticket.created_at),
    }