from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from datetime import datetime,timezone

app = FastAPI()

tickets_db = [
    {"id": 1, "movie_name": "Doctor Strange 3", "room_code": "IMAX-01", "quantity": 2, "status": "confirmed", "created_at": "2026-07-01T19:00:00Z"},
    {"id": 2, "movie_name": "Avatar 3", "room_code": "PREMIUM-02", "quantity": 1, "status": "confirmed", "created_at": "2026-07-01T20:15:00Z"}
]

class TicketSchema(BaseModel):
    movie_name: str = Field(...,min_length=1)
    room_code: str = Field(...,min_length=1)
    quantity: int = Field(ge=1,le=10)


def create_value(status_code: int, message: str, data=None, error=None, path:str=""):
    return{
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "path": path,
    }

@app.get("/tickets")
def get_ticket():
    return create_value(
        status_code=200,
        message="Lấy danh sách vé thành công!",
        data=tickets_db,
        error=None,
        path="/tickets"
    )

@app.post("/tickets")
def create_ticket(ticket: TicketSchema):
    for t in tickets_db:
        if (t["movie_name"] == ticket.movie_name and t["room_code"] == ticket.room_code):
            raise HTTPException(
                status_code=400,
                detail=create_value(
                    status_code=400,
                    message="Lỗi: Vé xem phim tại phòng chiếu đã được đặt!",
                    error="ERR-CINE-01: Ticket conflict for movie and room combination.",
                    path="/tickets",
                )
            )
    if tickets_db:
        new_id = max(t["id"] for t in tickets_db) + 1
    else:
        new_id = 1
    
    new_ticket = {
        "id": new_id,
        "movie_name": ticket.movie_name,
        "room_code": ticket.room_code,
        "quantity": ticket.quantity,
        "status": "Confirmed",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    tickets_db.append(new_ticket)
    return new_ticket