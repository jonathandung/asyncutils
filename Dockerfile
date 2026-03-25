FROM python:3.15-rc-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONPATH="/Users/Jonathan Dung/asyncutils"
WORKDIR /Users/Jonathan Dung/asyncutils
COPY dist/*.tar.gz .
COPY dist/*.whl .
RUN pip install --no-cache-dir *.tar.gz
RUN python -c "print(__import__('asyncutils').__version__.representation)"
ENTRYPOINT ["asyncutils"]
CMD ["-?"]