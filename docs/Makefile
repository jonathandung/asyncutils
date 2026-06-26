SPHINXOPTS ?=
SPHINXBUILD ?= sphinx-build
.PHONY: help Makefile
help:
	@$(SPHINXBUILD) -M help source build $(SPHINXOPTS) $(O)
%: Makefile
	@$(SPHINXBUILD) -M $@ source build $(SPHINXOPTS) $(O)
