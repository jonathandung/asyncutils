# Support Guidelines

Thank you for using asyncutils! This document outlines how to get help with this project.

Before jumping to seek support, do skim through [the readme](https://github.com/jonathandung/asyncutils#asyncutils).

## Bug Reports

If you've found a bug, please:

1. Check if it's already reported in [Issues](https://github.com/jonathandung/asyncutils/issues)
2. If so, participate meaningfully there
3. Open a new issue otherwise, possibly using the dedicated ``asyncutils bug`` sub-command to pre-fill information
4. Enter the required information into the issue form
5. Wait for review

## Feature Requests

Have an idea? We'd love to hear it!

- Search existing issues to avoid duplicates
- Explain the use case and expected behaviour
- Include examples in non-trivial cases

## Questions

### Community Support

- [GitHub Discussions](https://github.com/jonathandung/asyncutils/discussions)
- Stack Overflow: Tag questions with `[python]` and `[asyncutils]`

### Quick Questions

For quick questions, consider:

- Checking existing issues/discussions
- Reading the FAQ section below
- Asking in community channels

## Security Issues

**Never report security vulnerabilities publicly.**

See [the security policy](https://asyncutils.readthedocs.io/en/stable/security.html) for details.

## Common Issues & Solutions

### Installation Problems

Update your package installer, then try the following fixes:

```bash
uv pip install -U py-asyncutils # Upgrade
uv pip check # Check for dependency shenanigans
uv pip tree # Pretty print the pip packages dependency tree
uv tree # Show only the dependencies of this package
uv pip uninstall py-asyncutils && uv pip install py-asyncutils # Clean install
```

Other (slower) package managers:
<!-- cspell:disable -->
```bash
pip install -U pipx && pipx ensurepath # pipx, installed with pip
conda update py-asyncutils # conda
# pip
pip install -U pipdeptree && pipdeptree # Quite a bit more clutter than uv pip tree, showing a single package repeatedly
pipdeptree --packages py-asyncutils # Only this package as above
```
<!-- cspell:enable -->
### Import Errors

Check if asyncutils is installed:

```bash
# uv
uv pip show py-asyncutils
# pip
pip show py-asyncutils
# or
pip list | grep py-asyncutils
```

If the package is not working with python, perform the steps below:

```bash
# Check sys.path
python3 -c "print(*__import__('sys').path, sep='\n')"
# Check for package naming conflicts; following snippet should print altlocks, base, buckets, channels, cli, compete, config, console
# constants, context, events, exceptions, ... separated by newlines
python3 -c "print(*__import__('asyncutils').__all__, sep='\n')"
# If not loading site, repeat the above steps w/ python3 -Sc
```

## Response Times

As fast as I can; that is:

- Bug reports: 3 days
- Feature requests: Reviewed biweekly
- Security issues: 1 day
- General questions: Community-driven

I will try to make a post on the discussions page (e.g. hiatus announcement) and set my status to 'On vacation' or similar in case of inactivity
such that I cannot fulfil these promises or meet other deadlines I set myself.

## Remarks

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
