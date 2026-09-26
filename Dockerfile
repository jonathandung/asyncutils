FROM astral/uv:python3.15-rc-trixie-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 UV_SYSTEM_PYTHON=1
WORKDIR /opt/asyncutils
COPY . .
RUN uv sync --locked --no-default-groups
RUN V="$(asyncutils -v)" && if [ "$(python3 -c print(__import__('asyncutils').__version__.representation))" = "$V" ]; then echo "$V"; else echo "asyncutils binary and library version mismatch" && exit 1; fi
RUN asyncutils -h
ENTRYPOINT ["asyncutils"]
