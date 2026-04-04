docker rm -f rekenoef 2>/dev/null || true && \
docker run -d --restart=always --name rekenoef -p 8501:8501 streamlit-app
