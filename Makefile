.PHONY: test test-with-badges clean ruff install install-system install-silent watch type-check rmclog clog publish pre-commit venv help
TEST_MAXFAIL ?= 3
test:
	pytest -p asyncio-cooperative -p no:asyncio --no-cov --no-local-badge --maxfail $(TEST_MAXFAIL)
test-with-badges:
	pytest -p asyncio-cooperative -p no:asyncio --no-cov --maxfail 0 --local-badge-output-dir assets --local-badge-duration-max 10 --local-badge-generate duration skipped status warnings xfailed
	pytest -p asyncio -p no:asyncio-cooperative --maxfail 0 --local-badge-output-dir assets --local-badge-generate cov last-run
clean:
	rm -rf build dist py_asyncutils.egg-info .ruff_cache .pytest_cache .coverage .uv-stamp docs/build docs/source/api docs/source/help.rst docs/source/makefile-usage.rst
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.py[co]' -delete
	find . -type f -name '*.so' -delete
.uv-stamp:
	@if command -v uv >/dev/null 2>&1; then true;
	elif command -v curl >/dev/null 2>&1; then
		curl -LsSf https://astral.sh/uv/install.sh | sh;
	elif command -v wget >/dev/null 2>&1; then
		wget -qO- https://astral.sh/uv/install.sh | sh;
	else
		echo "curl or wget required to install uv" >&2
		exit 1
	fi
	(uv tool install -U ruff &&	uv tool install -U ty) 2>/dev/null
	touch .uv-stamp
venv: .uv-stamp
	uv venv
install: .uv-stamp
	uv pip install -Ue .[dev]
install-system: .uv-stamp
	uv pip install --system -Ue .[dev]
install-silent:
	$(MAKE) install > /dev/null
ruff: .uv-stamp
	ruff check
watch:
	ptw --runner "pytest" --onfail "echo 'Tests failed!'"
type-check: .uv-stamp
	ty check
rmclog:
	rm ChangeLog || true
clog: rmclog
	git log --pretty --numstat --summary > ChangeLog
publish: .uv-stamp
	uv build && uv publish
pre-commit: .uv-stamp
	pre-commit run --all-files
help:
	@cat make.help
