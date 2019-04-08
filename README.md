# Introduction
## Installation
On MacOS or Linux (I haven't figured it out on Windows yet), install with
```
pip install texnew
git clone https://github.com/alexrutar/texnew-templates ~/.texnew
```
Template-specific information can be found at [texnew-templates](https://github.com/alexrutar/texnew-templates).
Make sure your pip version is at least Python 3.7 (you can do this with `pip --version`); you might need to use `pip3` instead.

## Basic Usage
List existing templates with
```
texnew -l
```
Build a LaTeX file from a template:
```
texnew example.tex notes
```
Note that the `.tex` is optional - running `texnew example notes` is equivalent.
Get more syntax help with
```
texnew -h
```

## Other Capabilities
You can save user info in `.texnew/user/default.yaml` or `.texnew/user/private.yaml`; `private.yaml` is prioritized, if it exists.
The data saved in these files is automatically substituted into templates - see [Designing Templates](https://github.com/alexrutar/texnew-templates#designing-templates).
If neither user file exists, you will get a warning but the program will still generate a template (without substitutions).

You can change the template type of existing files, or update the file to reflect new macros in the template:
```
texnew example.tex asgn
cat "new content" >> example.tex
texnew -u example.tex notes
```
Updating preserves the content in the `file-specific preamble` and in `main document`.
Note that the comment dividers `% div_name ----...` should not be replicated or edited in order for updating to work (they are used to determine the different components of the file).
Your old file is saved in the same directory with `_n` appended to the name, where `n >= 0` is the smallest integer such that the new filename is unique.
(Note: the updating feature is unstable pre-2.0.)

If you make your own templates or edit macro files, run
```
texnew -c
```
to automatically compile all templates and check for LaTeX errors.
Note that the checker works by making a system call to `latexmk`; see the [latexmk documentation](https://mg.readthedocs.io/latexmk.html).
(This may or may not work on Windows.)

# Writing Templates
This has been relocated to the [texnew-templates](https://github.com/alexrutar/texnew-templates#designing-templates) repository.

# Using the Module
(to be written eventually)
To include:
- some link to general module documentation made with sphinx
- main classes, methods, using methods
- many code examples for this
- breakdowns of code used in texnew/scripts.py
