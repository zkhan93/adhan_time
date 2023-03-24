FROM python:3.10-slim-bullseye as prod
ENV PYHTONUNBUFFERED=1

RUN pip install --upgrade pip && pip install poetry

WORKDIR /code

COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false --local && \
  poetry install --no-root --no-interaction --no-ansi --without=dev
COPY . /code/
EXPOSE 80
ENTRYPOINT ["/code/scripts/run.sh"]

FROM prod as dev
RUN poetry install --no-root --no-interaction --no-ansi
