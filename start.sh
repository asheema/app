#!/bin/bash
# Start FastAPI in background, then Streamlit
uvicorn api:app --host 0.0.0.0 --port 8000 &
streamlit run app.py --server.port 10000 --server.address 0.0.0.0
