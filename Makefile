.PHONY: audit-deps build-docs changelog clean gen-badges gen-baseline help install install-silent lint lock pc release ruff sc tc test venv watch
AUTILSTESTMAXFAIL ?= 3
.DEFAULT_GOAL := help
O := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
.prek-stamp:
	@if command -v prek >/dev/null 2>&1; then true;
	elif command -v curl >/dev/null 2>&1; then
		curl -LsSf https://github.com/j178/prek/releases/download/v0.4.10/prek-installer.sh | sh
	elif command -v wget >/dev/null 2>&1; then
		wget -qO- https://github.com/j178/prek/releases/download/v0.4.10/prek-installer.sh | sh
	else
		echo "curl or wget required to install prek" >&2
		exit 1
	fi
	prek install -f
	touch .prek-stamp
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
	(uv tool install --force -U ruff &&	uv tool install --force -U ty) 2>/dev/null
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
	rm -rf .coverage .cspellcache .prek-stamp .pytest_cache .ruff_cache .uv-stamp build dist docs/build docs/source/api docs/source/help.rst docs/source/makefile-usage.rst py_asyncutils.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.py[codz]' -delete
gen-badges:
	pytest -p asyncio-cooperative -p no:asyncio --no-cov --local-badge-output-dir badges --local-badge-duration-max 10 --local-badge-generate duration skipped status xfailed
	pytest -p asyncio -p no:asyncio-cooperative --local-badge-output-dir badges --local-badge-generate last-run warnings
gen-baseline:
	detect-secrets scan > .secrets.baseline
help:
	@cat assets/mkhelp.txt
install: .prek-stamp .uv-stamp
	uv pip install -Ue .[dev]
install-silent:
	$(MAKE) install > /dev/null
lint: .uv-stamp
	ruff check
	ty check
	$(MAKE) sc
lock: .uv-stamp
	uv lock -U
pc: .prek-stamp
	prek run
release:
	if [[ ! $(read -p "You are about to create a release. Are you sure? (y/N) ") =~ ^([yY][eE][sS]|[yY])$ ]]; then
		echo "Release aborted."
		exit 1
	fi
	gh release create
ruff: .uv-stamp
	ruff check
sc:
	cspell .
tc: .uv-stamp
	ty check
test:
	pytest -p asyncio-cooperative -p no:asyncio --no-cov --no-local-badge --maxfail $(AUTILSTESTMAXFAIL)
venv: .uv-stamp
	uv venv
watch:
	ptw --runner "pytest" --onfail "echo 'Tests failed!'"
%::
	@true
