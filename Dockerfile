FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app

COPY ./model_augmented /app/model

RUN pip install spacy && \
    python -m spacy download fr_core_news_sm