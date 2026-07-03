# main.py
# Yeh FastAPI application ka entry point hai - server yahan se start hota hai

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_routes

# FastAPI app banate hain
app = FastAPI(title="Nexa AI", description="ChatGPT jaisa AI Chat Application")

# CORS Middleware - yeh frontend (HTML/JS) ko backend se baat karne ki permission deta hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router ko app mein include karte hain
app.include_router(auth_routes.router)


@app.get("/")
def root():
    return {"message": "Nexa AI Backend is running!"}


# main.py - yeh poora updated version hai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_routes, chat_routes

app = FastAPI(title="Nexa AI", description="ChatGPT jaisa AI Chat Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(chat_routes.router)

@app.get("/")
def root():
    return {"message": "Nexa AI Backend is running!"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_routes, chat_routes, message_routes

app = FastAPI(title="Nexa AI", description="ChatGPT jaisa AI Chat Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
app.include_router(message_routes.router)

@app.get("/")
def root():
    return {"message": "Nexa AI Backend is running!"}