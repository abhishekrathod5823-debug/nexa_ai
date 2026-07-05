from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth_routes, chat_routes, message_routes

# Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nexa AI API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
app.include_router(message_routes.router)

@app.get("/")
def root():
    return {"message": "Nexa AI Backend is running!"}
