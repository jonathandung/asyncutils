# Support Guidelines

Thank you for using asyncutils! This document outlines how to get help with this project.

Before jumping to seek support, do skim through **[README.md](https://github.com/jonathandung/asyncutils/blob/main/README.md)**.

## Bug Reports

If you've found a bug, please:

1. Check if it's already reported in [Issues](https://github.com/jonathandung/asyncutils/issues)
2. If not, create a new issue
3. Refer and adhere to the issue template chosen; otherwise, issue risks being closed without going through actual review

## Feature Requests

Have an idea? We'd love to hear it!

- Search existing issues to avoid duplicates
- Explain the use case and expected behavior
- Include examples unless you think the idea is a no-brainer

## Questions

### Community Support

- [**GitHub Discussions**](https://github.com/jonathandung/asyncutils/discussions)
- **Stack Overflow**: Tag questions with `[python]` and `[asyncutils]`

### Quick Questions

For quick questions, consider:

- Checking existing issues/discussions
- Reading the FAQ section below
- Asking in community channels

## Security Issues

**Never report security vulnerabilities publicly.**

See [SECURITY.md](SECURITY.md) for details.

## 🔧 Common Issues & Solutions

### Installation Problems

Update your package installer, then try the following fixes:

```bash
# Upgrade
pip install -U py-asyncutils

# Check for dependency shenanigans
pip check

# I personally also use:
pip install -U pipdeptree
pipdeptree # Prettily print the dependency graph
pipdeptree --packages py-asyncutils # Show only the dependents and dependencies of this package

# Clean install
pip uninstall py-asyncutils
pip install py-asyncutils

# If using pipx

pip install -U pipx
pipx ensurepath

# If using conda
conda update py-asyncutils

# If using uv
uv pip install -U py-asyncutils
```

### Import Errors

Check if asyncutils is installed:

```bash
pip list | grep py-asyncutils
```

If the package is not working with python, perform the steps below:

```bash
# Check sys.path
python -c "print(*__import__('sys').path, sep='\n')"
# Check for package naming conflicts; following snippet should print altlocks, base, buckets, caches, channels, cli, compete, config, console
# constants, context, events, exceptions, ... separated by newlines
python -c "print(*__import__('asyncutils').__all__, sep='\n')"
# If not loading site, repeat the above steps w/ python -Sc
```

## Version Compatibility

- Python 3.12+ required
- No dependencies outside development, which we're proud of
- This project is under active development (patch version is frequently bumped) that can have breaking changes

## Response Times

As fast as I can; that is:

- Bug reports: 3 days
- Feature requests: Reviewed biweekly
- Security issues: 1 day
- General questions: Community-driven

If the promises above are not met, and there was no relevant post on the discussions page (e.g. hiatus announcement) or my status was not set to 'On
vacation', that must have been a major oversight on my end.

## Closing remarks

Don't:

- Bump issues with +1 or "me too"
- Email maintainers unless urgent
- Ask about ETA of features/fixes
- Post API keys or passwords

Instead:

- React to issues
- Open discussions or issues, or a pull request if the problem is easily fixable
- Be patient

Once again, thank you for supporting this small project. Happy programming!
