.PHONY: test clean ruff install install-silent install-dev install-all watch type-check rmclog clog build publish pre-commit help
test:
	pytest
clean:
	rm -rf build dist asyncutils.egg-info .ruff_cache .pytest_cache .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.py[co]' -delete
	find . -type f -name '*.so' -delete
.uv-stamp:
	curl -LsSf https://astral.sh/uv/install.sh | sh
    uv tool install ruff
	uv tool install ty
	touch .uv-stamp
install: .uv-stamp
	uv pip install -e .
install-silent:
	$(MAKE) install > /dev/null
install-dev: .uv-stamp
	uv pip install -e .[dev]
install-all: .uv-stamp
	uv pip install -e .[all]
ruff: .uv-stamp
	ruff check .
watch:
	ptw --runner "make test" --onfail "echo 'Tests failed!'"
type-check:
	ty check
rmclog:
	rm ChangeLog || true
clog: rmclog
	git log --pretty --numstat --summary > ChangeLog
build:
	python3 -m build
publish: build
	twine upload dist/* --verbose --skip-existing
pre-commit:
	pre-commit run --all-files
help:
	@echo "Available targets:"
	@echo "  help           - Show this help message"
	@echo "  test           - Run tests with coverage"
	@echo "  clean          - Clean build artifacts and caches"
	@echo "  install        - Install the package in editable mode"
	@echo "  install-silent - The above without output"
	@echo "  install-dev    - Install the package with development dependencies"
	@echo "  install-all    - Install the package with all dependencies"
	@echo "  ruff           - Run the ruff linter"
	@echo "  watch          - Watch for changes and run tests automatically"
	@echo "  type-check     - Run ty for type checking"
	@echo "  rmclog         - Remove existing changelog file"
	@echo "  clog           - Generate changelog to file named ChangeLog from git history"
	@echo "  build          - Build the package distributions"
	@echo "  publish        - Publish the package to PyPI"
	@echo "  pre-commit     - Run pre-commit hooks on all files"