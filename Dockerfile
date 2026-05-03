# ============================================
# Multi-stage Dockerfile for Flask App
# ============================================

# Stage 1: Builder
FROM python:3.10-slim AS builder

WORKDIR /build

# Install build dependencies
COPY app/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (minimal image)
FROM python:3.10-slim AS runtime

# Create non-root user
RUN useradd -m -u 1001 appuser

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY app/app.py .

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add local packages to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 5000

CMD ["python", "app.py"]
