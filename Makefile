.DEFAULT_GOAL := help
.PHONY: badges bug build clean dclean docs help links lint lock log pc release run setup test
.SHELLFLAGS := -eo pipefail -c
.SILENT:
AUTESTMAXFAIL ?= 3
O := "$(wordlist 2,$(words $(MAKECMDGOALS)), $(MAKECMDGOALS))" "$(O)"
PREK_UV_SOURCE := none
SHELL := /bin/bash
.prek-stamp:
	if command -v prek >/dev/null 2>&1; then true; elif command -v curl >/dev/null 2>&1; then curl -LsSf https://github.com/j178/prek/releases/download/v0.5.6/prek-installer.sh | sh; elif command -v wget >/dev/null 2>&1; then wget -qO- https://github.com/j178/prek/releases/download/v0.5.6/prek-installer.sh | sh; else echo "curl or wget required to install prek" >&2; exit 1; fi
	prek install
	touch .prek-stamp
.uv-stamp:
	if command -v uv >/dev/null 2>&1; then true; elif command -v curl >/dev/null 2>&1; then curl -LsSf https://astral.sh/uv/install.sh | sh; elif command -v wget >/dev/null 2>&1; then wget -qO- https://astral.sh/uv/install.sh | sh; else echo "curl or wget required to install uv" >&2; exit 1; fi
	uv tool install ruff && uv tool install ty 2>/dev/null
	touch .uv-stamp
badges:
	pytest -p asyncio-cooperative -p no:asyncio --no-cov --local-badge-output-dir badges --local-badge-duration-max 10 --local-badge-generate duration skipped status xfailed
	pytest -p asyncio -p no:asyncio-cooperative --local-badge-output-dir badges --local-badge-generate last-run warnings
bug:
	asyncutils bug --open "$(O)"
build:
	docker build -t jonathandung/asyncutils:latest .
clean:
	rm -rf .coverage .cspellcache .prek-stamp .pytest_cache .ruff_cache .uv-stamp build dist docs/build docs/source/api docs/source/bug-help.rst docs/source/help.rst docs/source/makefile-usage.rst docs/source/ai-use.md docs/source/changelog.md docs/source/conduct.md docs/source/contributing.md docs/source/governance.md docs/source/roadmap.md docs/source/security.md docs/source/support.md py_asyncutils.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.py[co]' -delete
dclean:
	git clean -dxf
docs:
	scripts/generate.sh
	$(MAKE) -C docs html
help:
	cat assets/mkhelp.txt
links:
	scripts/generate.sh
	$(MAKE) -C docs linkcheck
lint: .uv-stamp
	echo "Running ruff..."
	ruff check
	echo "Running ty..."
	ty check
	if command -v cspell >/dev/null 2>&1; then echo "Running cspell..." && cspell .; fi
lock: .uv-stamp
	uv lock -U
log:
# cspell:disable-next-line
	git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
pc: .prek-stamp
	prek run -a
release:
	read -p "You are about to create a release. Are you sure? (y/N) " -n 1 -r; echo; if [[ $$REPLY =~ [Yy]$ ]]; then gh release create; else echo "Release aborted." >&2; exit 1; fi
run:
	docker run --rm -it jonathandung/asyncutils:latest
setup: .uv-stamp .prek-stamp
	uv sync
test:
	pytest -p asyncio-cooperative -p no:asyncio --no-cov --no-local-badge --maxfail "$(AUTESTMAXFAIL)"
%::
	true
