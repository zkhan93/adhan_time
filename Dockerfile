FROM python:3.10-slim-bullseye as prod

ENV PYHTONUNBUFFERED=1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN pip install --upgrade pip && pip install poetry

WORKDIR /code

COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false --local && \
  poetry install --no-root --no-interaction --no-ansi --without=dev
COPY . /code/
EXPOSE 8084
ENTRYPOINT ["/code/scripts/run.sh"]

FROM prod as dev
RUN poetry config virtualenvs.create false --local && \
  poetry install --no-root --no-interaction --no-ansi --with=dev
