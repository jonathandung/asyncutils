Issue Parameters
================

GitHub supports
`filling issue forms using parameters in the query string portion of a URL <https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms>`__.
If you use ``asyncutils bug --open``, you probably do not need the following since the
prompting and filling is done for you. However, one who wants to automate may not have
:mod:`asyncutils` on their system, or would like to suggest multiple features at once
(feature proposals are not supported by ``asyncutils bug``). The specific parameters
for each bug report type are detailed below.

Bug
---

* desc: bug description
* link: source code URL
* mre: minimal reproducible example
* expected: expected behaviour
* ss: screenshots
* pyv: Python version; required
* auv: library version; required
* os: operating system; required
* pkv: package version; required
* tb: error traceback
* cfg: library configuration
* logs: debug logs
* env: environment variables
* ctx: context

Documentation issue
-------------------

* links: links to faulty pages
* desc: problem description
* ctx: context

Feature request
---------------

* desc: feature description
* mot: motivation
* code: code snippets
* ss: screenshots
