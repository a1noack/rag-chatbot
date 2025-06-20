# ---- backend image ----
FROM python:3.10-slim
# Allow overriding pip cache and temp dirs via build args
ARG PIP_CACHE_DIR=/tmp/.cache/pip
ARG TMPDIR=/tmp
ENV PIP_CACHE_DIR=${PIP_CACHE_DIR} \
    TMPDIR=${TMPDIR}
RUN mkdir -p "$PIP_CACHE_DIR"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
