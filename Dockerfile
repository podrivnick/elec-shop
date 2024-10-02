FROM python:3.12.1-slim-bullseye as builder

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.8.2 && \
    poetry export -o requirements.prod.txt --without-hashes && \
    poetry export --with=dev -o requirements.dev.txt --without-hashes


ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python:3.12.1-slim-bullseye as dev


WORKDIR /elec-shop

COPY --from=builder requirements.dev.txt /elec-shop

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-dev \
                       gcc \
                       musl-dev \
                       libpq-dev \
                       nmap \
                       netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade --no-cache-dir pip==24.0 \
    && pip install --no-cache-dir poetry==1.8.2 \
    && pip install --no-cache-dir pip==24.0 \
    && pip install --no-cache-dir -r requirements.dev.txt


COPY . /elec-shop/

EXPOSE 8000
