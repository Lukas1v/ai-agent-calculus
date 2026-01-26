FROM ai-calculus-base

WORKDIR /app

COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt --system

COPY src/ ./src/
COPY .env .env

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
