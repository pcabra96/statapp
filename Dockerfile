# ---------------------------------------------------------------------------
# Dockerfile for StatApp
# ---------------------------------------------------------------------------
#
# Base image: python:3.11-slim
#   - "slim" strips dev tools and docs, shrinking the image from ~1 GB to ~130 MB.
#   - We pin to 3.11 (not "latest") so a future Python version can't silently
#     break our app.
#
# Build:  docker build -t statapp .
# Run:    docker run -p 8501:8501 statapp
# Open:   http://localhost:8501
# ---------------------------------------------------------------------------

FROM python:3.11-slim

# WORKDIR creates the directory if it doesn't exist and makes it the default
# for all subsequent RUN / CMD instructions.
WORKDIR /app

# Copy requirements first and install them BEFORE copying the rest of the code.
# Why? Docker builds layers in order and caches each layer. If we copy all
# files first, ANY code change (even a comment) would bust the pip layer and
# force a full re-install on the next build. Copying requirements.txt alone
# means pip only re-runs when the dependencies actually change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
COPY . .

# Streamlit listens on 8501 by default. EXPOSE documents this for readers
# and tools like Docker Compose — it does NOT open a firewall port on its own.
EXPOSE 8501

# Health check: Docker will ping this endpoint every 30 s.
# If it fails 3 times in a row, the container is marked "unhealthy".
# Render and other platforms use this to decide whether to restart the container.
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the app.
# --server.address=0.0.0.0  makes Streamlit listen on all network interfaces,
#                            not just localhost. Without this, the container is
#                            unreachable from outside — a very common gotcha.
# --server.port=8501         explicit port (matches EXPOSE above)
# --server.fileWatcherType=none  disables the file watcher that reruns the app
#                            on code changes. Unnecessary in production and
#                            saves a small amount of CPU.
CMD ["streamlit", "run", "app.py",
     "--server.address=0.0.0.0",
     "--server.port=8501",
     "--server.fileWatcherType=none"]
