#!/bin/bash
set -e
declare -a files=(
  "AI_USAGE_POLICY.md:ai-use.md"
  "CHANGELOG.md:changelog.md"
  "CODE_OF_CONDUCT.md:conduct.md"
  "COMPATIBILITY.rst:compat.rst"
  "CONTRIBUTING.md:contributing.md"
  "EXAMPLES.rst:examples.rst"
  "ROADMAP.md:roadmap.md"
  "SECURITY.md:security.md"
  "SUPPORT.md:support.md"
)
for mapping in "${files[@]}"; do
  src="${mapping%:*}"
  dst="${mapping#*:}"
  dest_path="docs/source/$dst"
  cp "$src" "$dest_path"
done
