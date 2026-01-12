#!/bin/bash

# 1. Start the FastAPI Backend in the background
# We run it on port 8000 (internal) and use & to keep it running
uvicorn main:app --host 0.0.0.0 --port 8000 &

# 2. Wait a few seconds for the backend to start
sleep 5

# 3. Start the Streamlit Frontend in the foreground
# Render gives us a specific port in the $PORT variable
streamlit run app.py --server.port $PORT --server.address 0.0.0.0