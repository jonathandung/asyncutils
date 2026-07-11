.PHONY: audit-deps build-docs changelog clean gen-badges gen-baseline help install install-silent pre-commit release ruff spellcheck test type-check venv watch
AUTILSTESTMAXFAIL ?= 3
.DEFAULT_GOAL := help
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
audit-deps: .uv-stamp
	uv audit --preview-features audit-command
build-docs:
	. scripts/unix/genhelp.sh
	. scripts/unix/genmakefileusage.sh
	make -C docs html -W
changelog:
# cspell:disable-next-line
	git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
clean:
	rm -rf build dist py_asyncutils.egg-info .cspellcache .ruff_cache .pytest_cache .coverage .uv-stamp docs/build docs/source/api docs/source/help.rst docs/source/makefile-usage.rst
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.py[codz]' -delete
gen-badges:
	pytest -p asyncio-cooperative -p no:asyncio --no-cov --local-badge-output-dir badges --local-badge-duration-max 10 --local-badge-generate duration skipped status xfailed
	pytest -p asyncio -p no:asyncio-cooperative --local-badge-output-dir badges --local-badge-generate last-run warnings
gen-baseline:
	detect-secrets scan > .secrets.baseline
help:
	@cat assets/mkhelp.txt
install: .uv-stamp
	uv pip install -Ue .[dev]
install-silent:
	$(MAKE) install > /dev/null
pre-commit:
	pre-commit run --all-files
release:
	gh release create
ruff: .uv-stamp
	ruff check
spellcheck:
	cspell lint .
test:
	pytest -p asyncio-cooperative -p no:asyncio --no-cov --no-local-badge --maxfail $(AUTILSTESTMAXFAIL)
type-check: .uv-stamp
	ty check
venv: .uv-stamp
	uv venv
watch:
	ptw --runner "pytest" --onfail "echo 'Tests failed!'"
