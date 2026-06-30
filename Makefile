.PHONY: build-docs changelog clean gen-badges gen-baseline help install install-silent install-system pre-commit regen-trie release ruff spellcheck test type-check venv watch
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
build-docs:
	bash ./scripts/unix/genhelp.sh
	bash ./scripts/unix/genmakefileusage.sh
	sphinx-build -W docs/source docs/build
changelog:
# cspell:disable-next-line
	git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
clean:
	rm -rf build dist py_asyncutils.egg-info .cspellcache .ruff_cache .pytest_cache .coverage .uv-stamp docs/build docs/source/api docs/source/help.rst docs/source/makefile-usage.rst
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.py[co]' -delete
	find . -type f -name '*.so' -delete
gen-badges:
	pytest -p asyncio-cooperative -p no:asyncio --no-cov --local-badge-output-dir badges --local-badge-duration-max 10 --local-badge-generate duration skipped status xfailed
	pytest -p asyncio -p no:asyncio-cooperative --local-badge-output-dir badges --local-badge-generate cov last-run warnings
gen-baseline:
	detect-secrets scan > .secrets.baseline
help:
	@cat assets/mkhelp.txt
install: .uv-stamp
	uv pip install -Ue .[dev]
install-silent:
	$(MAKE) install > /dev/null
install-system: .uv-stamp
	uv pip install --system -Ue .[dev]
pre-commit:
	pre-commit run --all-files
regen-trie:
	cspell-tools compile-trie ./assets/words.txt -o ./assets
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
