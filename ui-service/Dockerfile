FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY UIDemo.py .

EXPOSE 7860

CMD ["python", "UIDemo.py"]