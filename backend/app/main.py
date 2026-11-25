"""Syncra demo API. Uses in-memory storage so it runs without external services.
For production, replace the demo auth/store with Supabase and enforce database RLS.
"""
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Syncra API", version="1.0.0", description="Local demo API for the Syncra campus events platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS: dict[str, dict] = {}
TOKENS: dict[str, str] = {}
PASSWORDS: dict[str, str] = {}
EVENTS: dict[str, dict] = {
    "event-art-talk": {"id": "event-art-talk", "title": "Art Talk", "club": "Art Club", "date": "2026-12-04", "time": "14:00", "venue": "Auditorium A", "description": "A conversation about creativity and design.", "capacity": 120, "registered": 38, "status": "approved"},
    "event-hackathon": {"id": "event-hackathon", "title": "Tech Hackathon", "club": "Tech Club", "date": "2026-12-08", "time": "09:00", "venue": "Innovation Lab", "description": "Build, learn and collaborate in a campus hackathon.", "capacity": 80, "registered": 54, "status": "approved"},
}
BUDGETS: dict[str, dict] = {}
NOTIFICATIONS: dict[str, list[dict]] = {}
VENUES: dict[str, dict] = {
    "auditorium-a": {"id": "auditorium-a", "name": "Auditorium A", "type": "auditorium", "capacity": 250, "building": "Main Block", "floor": "Ground", "bookable": True},
    "innovation-lab": {"id": "innovation-lab", "name": "Innovation Lab", "type": "lab", "capacity": 100, "building": "Technology Block", "floor": "2", "bookable": True},
}

class Signup(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: Literal["student", "president", "faculty"] = "student"
    student_id: str | None = None

class Login(BaseModel):
    email: EmailStr
    password: str

class EventCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    club: str = "Campus Club"
    date: str
    time: str
    venue: str
    description: str = ""
    capacity: int = Field(default=100, gt=0)

class BudgetItem(BaseModel):
    category: Literal["venue", "food", "prizes", "marketing", "equipment", "honorarium", "misc"]
    amount: float = Field(gt=0)
    justification: str = ""

class BudgetRequest(BaseModel):
    event_id: str
    total_amount: float = Field(gt=0)
    items: list[BudgetItem]
    remarks: str | None = None

async def current_user(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Please log in to continue")
    token = authorization.split(" ", 1)[1]
    user_id = TOKENS.get(token)
    if not user_id or user_id not in USERS:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again")
    return USERS[user_id]

def require_role(*roles: str):
    async def checker(user: dict = Depends(current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Your account does not have permission for this action")
        return user
    return checker

@app.get("/")
async def root():
    return {"name": "Syncra API", "status": "ok", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.post("/api/v1/auth/signup", status_code=201)
async def signup(payload: Signup):
    email = str(payload.email).lower()
    if any(u["email"] == email for u in USERS.values()):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user_id = str(uuid4())
    user = {"id": user_id, "email": email, "role": payload.role, "student_id": payload.student_id}
    USERS[user_id] = user
    PASSWORDS[user_id] = payload.password
    token = str(uuid4())
    TOKENS[token] = user_id
    NOTIFICATIONS[user_id] = [{"id": str(uuid4()), "title": "Welcome to Syncra", "message": "Your account is ready. Explore campus events!", "read": False, "created_at": datetime.now(timezone.utc).isoformat()}]
    return {"access_token": token, "token_type": "bearer", "user": user}

@app.post("/api/v1/auth/login")
async def login(payload: Login):
    email = str(payload.email).lower()
    user = next((u for u in USERS.values() if u["email"] == email), None)
    if user and PASSWORDS.get(user["id"]) != payload.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user:
        # A convenient local-demo account; signup is still available for any role.
        if email.endswith("@example.edu") and payload.password == "syncra123":
            uid = str(uuid4()); role = "faculty" if email.startswith("faculty") else "president" if email.startswith("president") else "student"
            user = {"id": uid, "email": email, "role": role, "student_id": None}; USERS[uid] = user; PASSWORDS[uid] = payload.password; NOTIFICATIONS[uid] = []
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password. Sign up first or use the demo account.")
    token = str(uuid4()); TOKENS[token] = user["id"]
    return {"access_token": token, "token_type": "bearer", "user": user}

@app.get("/api/v1/auth/me")
async def me(user: dict = Depends(current_user)):
    return user

@app.get("/api/v1/public/events")
async def public_events():
    return list(EVENTS.values())

@app.get("/api/v1/events")
async def events(user: dict = Depends(current_user)):
    return list(EVENTS.values())

@app.post("/api/v1/events", status_code=201)
async def create_event(payload: EventCreate, user: dict = Depends(require_role("president", "faculty"))):
    event_id = str(uuid4())
    event = {"id": event_id, **payload.model_dump(), "registered": 0, "status": "pending", "created_by": user["id"]}
    EVENTS[event_id] = event
    return event

@app.post("/api/v1/events/{event_id}/register")
async def register_event(event_id: str, user: dict = Depends(require_role("student", "president", "faculty"))):
    event = EVENTS.get(event_id)
    if not event: raise HTTPException(status_code=404, detail="Event not found")
    if event["registered"] >= event["capacity"]: raise HTTPException(status_code=409, detail="This event is full")
    event["registered"] += 1
    return {"message": "Registration successful", "event": event}

@app.get("/api/v1/my/events")
async def my_events(user: dict = Depends(current_user)):
    return [e for e in EVENTS.values() if e.get("created_by") == user["id"]]

@app.post("/api/v1/budget/request", status_code=201)
async def submit_budget(request: BudgetRequest, user: dict = Depends(require_role("president"))):
    if request.event_id not in EVENTS: raise HTTPException(status_code=404, detail="Event not found")
    ceilings = {"venue": 2000, "food": 1000, "prizes": 800, "marketing": 500, "equipment": 700, "honorarium": 600, "misc": 300}
    recommendations = [{"action": "reduce", "reason": f"{i.category.title()} exceeds the suggested ${ceilings[i.category]:,.0f} limit"} for i in request.items if i.amount > ceilings[i.category]]
    if request.total_amount > 5000: recommendations.append({"action": "revision", "reason": "Total budget exceeds the suggested $5,000 limit"})
    if not recommendations: recommendations = [{"action": "approve", "reason": "Budget is within the suggested limits"}]
    result = {**request.model_dump(), "status": "pending", "recommendations": recommendations, "submitted_by": user["id"]}
    BUDGETS[request.event_id] = result
    return result

@app.get("/api/v1/budget/requests")
async def list_budgets(user: dict = Depends(require_role("faculty"))):
    return list(BUDGETS.values())

@app.get("/api/v1/budget/request/{event_id}")
async def get_budget(event_id: str, user: dict = Depends(current_user)):
    result = BUDGETS.get(event_id)
    if not result: raise HTTPException(status_code=404, detail="Budget not found")
    return result

@app.post("/api/v1/budget/decision/{event_id}")
async def budget_decision(event_id: str, decision: Literal["approve", "reduce", "revision", "reject"] = "approve", user: dict = Depends(require_role("faculty"))):
    result = BUDGETS.get(event_id)
    if not result: raise HTTPException(status_code=404, detail="Budget not found")
    result["status"] = decision
    return {"message": f"Budget {decision}", "budget": result}

@app.get("/api/v1/notifications")
async def notifications(user: dict = Depends(current_user)):
    return NOTIFICATIONS.get(user["id"], [])

@app.post("/api/v1/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str, user: dict = Depends(current_user)):
    item = next((n for n in NOTIFICATIONS.get(user["id"], []) if n["id"] == notification_id), None)
    if not item: raise HTTPException(status_code=404, detail="Notification not found")
    item["read"] = True
    return item

@app.get("/api/v1/venues")
async def list_venues(user: dict = Depends(current_user)):
    return list(VENUES.values())
