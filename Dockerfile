FROM python:3.11-slim

# Set up user and home directory for Hugging Face compatibility
RUN useradd -m -u 1000 user
WORKDIR /home/user/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY --chown=user requirements_render.txt .
RUN pip install --no-cache-dir -r requirements_render.txt

# Copy all application files
COPY --chown=user . .

# Set environment variables
ENV PORT=7860
ENV SIMULATION_MODE=True

# Expose port
EXPOSE 7860

# Run the app
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:7860", "perfect_indian_app:app"]
