# Roadmap

This file provides an overview of the direction towards which this project is heading.

Current version: 0.8.18

## 0.9

- Create a test suite for the module
- Separate type annotations from iters.py into iters.pyi
- Further enrich the command line

## 1.0

- Finalize the API
- Document each submodule extensively
- Include proper CI workflows (travis/circle)

## 1.x

- Enhance the test suite
- Incorporate user feature requests
- Increment major version once serious bugs are found in 3 functions or more that necessitate their removal

## 2.x

- The python 3.15-only analog to 1.x releases, which will be released at the same time as them.

## 3.0

- Major feature additions, with more focus on low-level stuff
- Comprehensive bugfixes
- Merge the dev branch into the main branch in one big refactor

## 3.x

- Ramp up coverage to 90%
- Publish docker images
- Deprecate <= 3.12 compatibility module

## 4.0

- Deprecate <=3.13 compatibility module
- New features
- Remove/supersede overly inefficient or faulty patterns

## 5.0 (2028)

- Make the python 3.15-only branch the main branch as 3.12 supposedly reaches EOL

## 6.0 (2029)

- Drop support for python 3.13 entirely as it reaches EOL

## 7.0 (2030)

- Drop support for python 3.14; integrate lazy imports fully
