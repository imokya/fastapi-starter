#!/bin/bash

# 启动FastAPI应用
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
