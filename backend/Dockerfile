FROM pytorch/pytorch:2.0.0-cuda12.2-cudnn8-runtime
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]