# Python WSGI Auth

A simple demo project showcasing **user authentication** (registration & login) with a minimal **Python WSGI backend** and a static frontend.  
Users are stored locally in a JSON file (`userInfo.json`).  

⚠️ **Note:** This project is educational and not intended for production use. Passwords are stored in plain text (for demo purposes only).  


---

## Backend Setup

### 1. Create and activate virtual environment
```bash
cd backend

# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate
```

### 2. Run backend server
```bash
python main.py
```

Server will start on:  
http://127.0.0.1:8000  


## Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start local preview server
npm run preview
```
---

## Features

- User **registration** with validation  
- User **login** with email & password check  
- Data persistence via JSON (`userInfo.json`)  
- CORS enabled for frontend-backend communication  


## Tech Stack

- **Backend:** Python (WSGI, wsgiref)  
- **Frontend:** React + TypeScript (prebuilt into static files)  
- **Storage:** JSON file  


