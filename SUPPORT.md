# Support Guidelines

Thank you for using asyncutils! This document outlines how to get help with this project.

Before jumping to seek support, please read through **[README.md](https://github.com/jonathandung/asyncutils/blob/main/README.md)**.

## Bug Reports

If you've found a bug, please:

1. Check if it's already reported in [Issues](https://github.com/jonathandung/asyncutils/issues)
2. If not, create a new issue
3. Include:

    - Python version tag (`python -VV`)
    - asyncutils version (`python -m asyncutils -v`)
    - Operating system
    - Package version (`pip show py-asyncutils` or `conda list py-asyncutils`)
    - Minimal reproducible example
    - Full error traceback

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
echo $? # Should be 0

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

If the package is not working with python -S, perform the steps below:

```bash
# Check sys.path
python -S -c "print(*__import__('sys').path, sep='\n')"
# Check for package naming conflicts; following snippet should print altlocks, base, buckets, caches, channels, cli, compete, config, console
# constants, context, events, exceptions, ... separated by newlines
python -S -c "print(*dir(__import__('asyncutils')), sep='\n')"
```

## Version Compatibility

- Python 3.12+ required
- No dependencies outside development, which we're proud of
- This project is under active development (new patch versions daily) that can have breaking changes

## Response Times

As fast as the creator (currently the sole maintainer) can; that is:

- Bug reports: 3 days
- Feature requests: Reviewed biweekly
- Security issues: 1 day
- General questions: Hopefully community-driven

At this stage, presume the creator dead if:

- promises above are not met, and
- there was no relevant post on the discussions page (e.g. hiatus announcement)

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
