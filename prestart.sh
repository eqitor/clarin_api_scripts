#! /usr/bin/env bash
python app/backend_pre_start.py
python app/initial_data.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 80
