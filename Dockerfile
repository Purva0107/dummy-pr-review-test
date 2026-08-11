FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml README.md ./
COPY src ./src
COPY scripts ./scripts
ENV PYTHONPATH=/app/src
ENV ACME_DATABASE_URL=sqlite:////app/data/orders.db
RUN mkdir -p /app/data
EXPOSE 8000
CMD ["uvicorn", "acme_orders.main:app", "--host", "0.0.0.0", "--port", "8000"]
