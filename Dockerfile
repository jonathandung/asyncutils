FROM astral/uv:python3.15-rc-trixie-slim
RUN groupadd -r au && useradd -r -g au -m -s /sbin/nologin asyncutils
ENV PATH="/opt/asyncutils/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_LOCKED=1 UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=never
WORKDIR /opt/asyncutils
COPY uv.lock pyproject.toml ./
RUN uv sync --no-install-project
COPY . .
RUN chown -R asyncutils:au .
RUN uv sync
USER asyncutils
RUN V="$(asyncutils -v)" && if [ "$(python -c 'import asyncutils as a; print(a.__version__.representation)')" = "$V" ]; then echo "$V"; else echo "asyncutils binary and library version mismatch" >&2 && exit 1; fi
ENTRYPOINT ["asyncutils"]
