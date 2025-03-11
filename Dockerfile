FROM python:3.12-slim

RUN apt-get update && apt-get install -y libmagic1

RUN useradd -m -r user && \
    mkdir /test_task && \
    chown -R user /test_task

WORKDIR /test_task

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY Pipfile Pipfile.lock /test_task/
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --system

COPY --chown=user:user . .

USER user

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000 --forwarded-allow-ips '*'"]