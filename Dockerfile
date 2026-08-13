FROM python:3.15-rc-slim-bookworm
# cspell:disable-next-line
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY dist/*.tar.gz .
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN uv venv
RUN uv pip install --frozen --no-cache *.tar.gz
RUN rm -rf *.tar.gz
RUN python3 -c "print(__import__('asyncutils').__version__.representation)"
RUN asyncutils -h
ENTRYPOINT ["asyncutils"]
