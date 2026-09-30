FROM astral/uv:python3.15-rc-trixie-slim
WORKDIR /opt/asyncutils
RUN groupadd -r au && useradd -r -g au -m -s /usr/sbin/nologin asyncutils
ENV PATH="/opt/asyncutils/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_LOCKED=1 UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=never
COPY uv.lock pyproject.toml README.md ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --no-install-project
COPY --chown=asyncutils:au . .
RUN uv sync
USER asyncutils
ENTRYPOINT ["asyncutils"]
