.PHONY: test clean ruff install install-silent install-dev install-all watch type-check stubtest rmclog clog build publish
test: pytest tests/ -v --cov asyncutils --cov-report xml --cov-fail-under 52 -n auto
clean:
  rm -rf build dist asyncutils.egg-info .pytest_cache .mypy_cache .coverage
  find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
  find . -type f -name '*.py[co]' -delete
  find . -type f -name '*.so' -delete
install: pip install -e .
install-silent: pip install -e . > /dev/null
install-dev: pip install -e .[dev]
install-all: pip install -e .[all]
ruff: ruff check .
watch: ptw --runner "make test" --onfail "echo 'Tests failed!'"
type-check: mypy asyncutils
stubtest: stubtest asyncutils --allowlist=allowlist.txt --strict-type-check-only
rmclog: rm ChangeLog || true
clog:
  rmclog
  git log --pretty --numstat --summary > ChangeLog
build: python3 -m build
publish:
  build
  twine upload dist/* --verbose --skip-existing