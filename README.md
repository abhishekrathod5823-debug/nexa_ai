<div align="center">

# 🤖 Nexa AI

### A full-stack AI chat application built with FastAPI, MySQL, and Groq LLM

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Netlify-00C7B7?style=for-the-badge&logo=netlify&logoColor=white)](https://comforting-cascaron-2bf29b.netlify.app)
[![Backend](https://img.shields.io/badge/Backend-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://nexa-ai-s8w0.onrender.com)
[![Database](https://img.shields.io/badge/Database-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-9.4-4479A1?style=flat-square&logo=mysql&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

</div>

---

## 📖 About

**Nexa AI** is a production-ready AI chat application inspired by ChatGPT. It supports multilingual conversations (Hindi, English, and Hinglish), features a unique circular gallery for chat history, smooth typing animations, JWT-based authentication, and persistent chat storage in MySQL.

Built as a complete full-stack project — from database design to live deployment.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Authentication** | Secure signup & login with JWT tokens and bcrypt password hashing |
| 💬 **AI Chat** | Real-time conversations powered by Groq LLM (Llama 3.3 70B) |
| 🌐 **Multilingual** | Supports Hindi, English, and Hinglish responses |
| 🗂️ **Chat History** | Circular gallery UI to browse and reopen past conversations |
| ✏️ **Chat Management** | Create, rename, and delete conversations |
| 🎨 **Modern UI** | Dark theme, glassmorphism design, smooth animations |
| 📱 **Responsive** | Works on desktop and mobile browsers |
| 🔒 **Secure** | SQL injection protection, input validation, environment variables |

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** — High-performance Python web framework
- **SQLAlchemy** — ORM for database interactions
- **PyMySQL** — MySQL database driver
- **Groq API** — AI responses via Llama 3.3 70B model
- **JWT + bcrypt** — Secure authentication
- **Uvicorn** — ASGI server

### Frontend
- **HTML5, CSS3, JavaScript** — Vanilla frontend (no framework)
- **Circular Gallery** — Custom physics-based animation for chat history
- **Space Grotesk** — Google Fonts typography

### Database
- **MySQL** — Relational database with 3 tables: `users`, `chats`, `messages`

### Deployment
- **Netlify** — Frontend hosting
- **Render** — Backend hosting (FastAPI server)
- **Railway** — MySQL database hosting

---

## 📁 Project Structure

```
Nexa AI/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth_routes.py      # Signup & Login APIs
│   │   │   ├── chat_routes.py      # Chat CRUD APIs
│   │   │   └── message_routes.py   # Message & AI response APIs
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── database.py             # MySQL connection setup
│   │   ├── models.py               # SQLAlchemy table models
│   │   ├── schemas.py              # Pydantic request/response schemas
│   │   ├── auth.py                 # JWT & bcrypt logic
│   │   └── config.py               # Environment variable loader
│   ├── venv/                       # Virtual environment
│   ├── .env                        # Secret keys (not committed)
│   ├── requirements.txt            # Python dependencies
│   └── runtime.txt                 # Python version for Render
└── frontend/
    ├── index.html                  # Login page
    ├── signup.html                 # Registration page
    └── dashboard.html              # Main app (gallery + chat)
```

---

## 🗄️ Database Schema

```sql
-- Users table
CREATE TABLE users (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    username     VARCHAR(50)  NOT NULL,
    email        VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chats table
CREATE TABLE chats (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL,
    title      VARCHAR(255) NOT NULL DEFAULT 'New Chat',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Messages table
CREATE TABLE messages (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    chat_id    INT NOT NULL,
    sender     ENUM('user', 'ai') NOT NULL,
    content    TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
);
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- MySQL (XAMPP / WAMP)
- Git

### 1. Clone the repository
```bash
git clone https://github.com/your-username/nexa-ai.git
cd nexa-ai
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file inside the `backend/` folder:
```env
DB_HOST=*******
DB_PORT==*******
DB_USER==*******
DB_PASSWORD=
DB_NAME=nexa_ai

JWT_SECRET==*******
JWT_ALGORITHM==*******
JWT_EXPIRE_MINUTES==*******

GROQ_API_KEY==*******
```

> **Get a free Groq API key:** https://console.groq.com

### 4. Create MySQL database
Open phpMyAdmin or MySQL CLI and run:
```sql
CREATE DATABASE nexa_ai;
```
Tables will be created automatically when the server starts.

### 5. Start the backend server
```bash
uvicorn app.main:app --reload
```
Backend runs at: `http://127.0.0.1:8000`
API docs available at: `http://127.0.0.1:8000/docs`

### 6. Open the frontend
Open `frontend/index.html` in your browser using VS Code Live Server or any local server.

---

## 🌐 API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/signup` | Register a new user |
| `POST` | `/auth/login` | Login and receive JWT token |

### Chats
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/chats/` | Get all chats for current user |
| `POST` | `/chats/` | Create a new chat |
| `GET` | `/chats/{id}` | Get a specific chat |
| `PUT` | `/chats/{id}/rename` | Rename a chat |
| `DELETE` | `/chats/{id}` | Delete a chat |

### Messages
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/chats/{id}/messages` | Send a message and get AI response |
| `GET` | `/chats/{id}/messages` | Get all messages in a chat |

---

## 🚢 Deployment

This project is deployed using three free platforms:

| Service | Platform | URL |
|---|---|---|
| Frontend | Netlify | Auto-deploy from GitHub |
| Backend | Render | Auto-deploy from GitHub |
| Database | Railway | Managed MySQL instance |

### Environment Variables on Render
Set these in Render → Environment:
```
DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
GROQ_API_KEY, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES
```

---

## 📸 Screenshots

> _Add screenshots of your login page, dashboard, and chat window here_

---

## 🔒 Security Features

- Passwords hashed with **bcrypt** (never stored in plain text)
- **JWT tokens** for stateless authentication (24-hour expiry)
- **CORS** configured for allowed origins only
- **Input validation** via Pydantic schemas
- **SQL injection protection** via SQLAlchemy ORM
- Sensitive keys stored in **environment variables** (never in code)

---

## 🧑‍💻 Author

**Abhishek Rathod**

> Built as a complete full-stack learning project — from zero to production deployment.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ using FastAPI + Groq AI

⭐ Star this repo if you found it helpful!

</div>
