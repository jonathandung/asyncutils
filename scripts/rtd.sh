#!/bin/bash
set -e
declare -a f=(
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
for m in "${f[@]}"; do
  cp "${m%:*}" "docs/source/${m#*:}"
done
