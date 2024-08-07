FROM python:3.9-slim as base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests
COPY main.py .

FROM base as test
RUN pip install pytest pytest-asyncio
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:///./test.db
CMD ["pytest", "tests"]

FROM base as production
CMD ["python", "main.py"]