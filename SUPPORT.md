# Support Guidelines

Thank you for using asyncutils! This document outlines how to get help with this project.

Before jumping to seek support, please check **[README.md](https://github.com/jonathandung/asyncutils/blob/dev/README.md)** for a basic usage and installation guide.

## Bug Reports

If you've found a bug, please:

1. Check if it's already reported in [Issues](https://github.com/jonathandung/asyncutils/issues)
2. If not, create a new issue
3. Include:

    - Python version (`python --version`)
    - asyncutils version (`autils -v`)
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

```bash
# Upgrade pip
python -m pip install -U pip

# Upgrade

pip install -U py-asyncutils

# Clean install
pip uninstall py-asyncutils
pip install py-asyncutils

# If using conda
conda update py-asyncutils
```

### Import Errors

```bash
# Check if installed
pip list | grep py-asyncutils
# Check sys.path
python -c "print(*__import__('sys').path, sep='\n')"
# Check for package naming conflicts; following snippet should print altlocks, base, buckets, caches, channels, cli, compete, config, console, constants, # context, ... separated by newlines
python -c "print(*dir(__import__('asyncutils')), sep='\n')"
```

## Version Compatibility

- Python 3.15+ required
- No dependencies outside development, which we're proud of
- Maybe use virtual environments

## Response Times

As fast as the creator (currently the sole maintainer) can; that is:

- Bug reports: 3 days
- Feature requests: Reviewed biweekly
- Security issues: 1 day
- General questions: Hopefully community-driven

## Closing remarks

Don't:

- Bump issues with +1 or "me too"
- Email maintainers unless urgent
- Ask about ETA about features/fixes
- Post API keys or passwords

Instead:

- React to issues
- Open discussions or issues, or a pull request if the problem is easily fixable
- Be patient; at this stage, presume me dead if the response times are not met and I did not post about a hiatus on the discussions page

Once again, thank you for supporting this small project. Happy programming!
