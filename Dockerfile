FROM python:3.15.0rc2-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /opt/asyncutils
COPY . .
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN uv venv
ENV PATH="/opt/asyncutils/.venv/bin:$PATH"
RUN uv sync --frozen --no-default-groups
RUN python3 -c "print(__import__('asyncutils').__version__.representation)"
RUN asyncutils -h
ENTRYPOINT ["asyncutils"]
