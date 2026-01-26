#!/bin/bash

echo "Step 1: Building base image from devcontainer..."
docker build --no-cache -t ai-calculus-base -f .devcontainer/Dockerfile .

echo "Step 2: Building production Streamlit app image..."
docker build -t streamlit-app .

echo "Done! To run the app, use:"
echo "  docker run -d -p 8501:8501 --restart=always --name ai-calculus streamlit-app "
