FROM python:3.11.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_USER=appuser

COPY pyproject.toml .

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

RUN mkdir -p /home/${APP_USER} && \
    echo "${APP_USER}:x:1001:1001:App User,,,:/home/${APP_USER}:/bin/bash" >> /etc/passwd && \
    echo "${APP_USER}:x:1000:" >> /etc/group && \
    chown -R 1001:1001 /home/${APP_USER} && \
    mkdir -p /var/app

WORKDIR /home/${APP_USER}

COPY . .

USER ${APP_USER}

ENTRYPOINT ["/bin/bash", "-c"]

CMD ["tail", "-f", "/dev/null"]