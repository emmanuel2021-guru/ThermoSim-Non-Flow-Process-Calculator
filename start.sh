#!/bin/bash

# 1. Start the FastAPI Backend
# We 'cd' into backend so that imports like "from utils import..." work correctly
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 &
cd ..

# 2. Wait for backend to initialize
sleep 5

# 3. Start the Streamlit Frontend
# Use slash '/' for the path, not dot '.'
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0