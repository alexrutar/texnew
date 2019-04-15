# Introduction
## Installation
On MacOS or Linux (I'm not sure about Windows yet), install with
```
pip install texnew
git clone https://github.com/alexrutar/texnew-templates ~/.texnew
```
Template-specific information can be found at [texnew-templates](https://github.com/alexrutar/texnew-templates).
Make sure your pip version is at least Python 3.7 (you can do this with `pip --version`); you might need to use `pip3` instead.

## Basic Usage
List existing templates with
```
texnew info -l
```
Build a LaTeX file from a template:
```
texnew new example.tex notes
```
The `.tex` is optional: running texnew new example notes` is equivalent.
Get more syntax help with `texnew {new,update,check,info} -h`; for example
```
texnew -h
texnew new -h
...
```

## Other Capabilities
You can save user info in `.texnew/user/default.yaml` or `.texnew/user/private.yaml`; `private.yaml` is prioritized, if it exists.
The data saved in these files is automatically substituted into templates - see [Designing Templates](https://github.com/alexrutar/texnew-templates#designing-templates).
If neither user file exists, you will get a warning but the program will still generate a template (without substitutions).

You can change the template type of existing files, or update the file to reflect new macros in the template:
```
texnew new example.tex asgn
cat "new content" >> example.tex
texnew update example.tex notes
```
Updating preserves the content in the `file-specific preamble` and in `main document`.
Note that the comment dividers `% div_name ----...` should not be replicated or edited in order for updating to work (they are used to determine the different components of the file).
Your old file is saved in the same directory with `_n` appended to the name, where `n >= 0` is the smallest integer such that the new filename is unique.

If you make your own templates or edit macro files, run
```
texnew check --all
```
to automatically compile all templates and check for LaTeX errors.
Run
```
texnew check template_name_1 template_name_2 ...
```
to test a specific list of templates.
Run
```
texnew check -p package_1 package_2 ...
```
to check every template from a given package.

Note that the checker works by making a system call to `latexmk`; see the [latexmk documentation](https://mg.readthedocs.io/latexmk.html).
You'll have to install this separately to use this functionality.
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
