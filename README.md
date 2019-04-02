# Introduction
## Installation
On MacOS or Linux (I haven't figured it out on Windows yet), install with
```
pip install texnew
cd ~
git clone https://github.com/alexrutar/texnew-templates .texnew
```
Template-specific information can be found at [texnew-templates](https://github.com/alexrutar/texnew-templates).
Make sure your pip version is at least (python 3.7) with `pip --version`; You might need to use `pip3` instead.

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
The data saved in these files is automatically substituted into templates - see [Designing Templates](#Designing-Templates).
If neither user file exists, you will get a warning but the program will still generate a template (without substitutions).

You can change the template type of existing templates:
```
texnew example.tex asgn
cat "new content" >> example.tex
texnew -u example.tex notes
```
Updating preserves the content in the `file-specific preamble` and in `main document`.
Note that the comment dividers `% div_name ----...` should not be replicated or edited in order for updating to work (or weird things will happen).
Your old file is saved in the same directory with `_old` appended to the name.
(Note: this is unstable pre-2.0.)

If you make your own templates or edit macro files, run
```
texnew -c
```
to automatically compile all templates and check for LaTeX errors.
Note that the checker works by making a system call to `latexmk`; see the [latexmk documentation](https://mg.readthedocs.io/latexmk.html).
(This may or may not work on Windows.)

# Designing Templates
Templates are organized into template sets which can be found in `.texnew/share`.
If you want to make your own template set, the easiest way is to copy the structure in `base`.
Template files are placed in the `templates` directory.
There are three (mandatory) options to be included in the template:
 - `doctype` can be any valid LaTeX document type (e.g. article, book)
 - `formatting` must be any filename (without extension) defined in Formatting
 - `macros` must be any filename (without extension) defined in Macros.
Additionally, you can define any substitution variables within the template - note that template-defined variables will override any user-defined variables.

## Template set directory structure
See `share/base` for the default example.
2. Macros: `macros/*`
    - Macro files stored here are accessed by the `macro` option in the templates. You can add your own macros, or pretty much whatever you want here.

3. Formatting: `formatting/*.tex`
    - Formatting files stored here are accessed by the `formatting` option in the templates. I've generally used them to define formatting for the file appearance (fonts, titlepages, etc).
    They must include `\begin{document}`; the `\end{docment}` label is automatically placed afterwards.
    - Wherever `<+key+>` appears in a formatting document, they are automatically replaced by the relevant info in the `user.yaml` file or the `template.yaml` file.
    `key` can be any string. You can define new keys.

4. Defaults: `defaults/doctype.tex` `defaults/packages.tex` `defaults/macros.tex`
    - Default files are loaded every time, regardless of the template used. Don't change the file names or weird things will happen, but feel free to change the defaults to whatever you want. `doctype.tex` must have the document class, and the tag `<+doctype+>` is automatically substituted by the defined value in a template. `macros.tex` is for default macros, and `packages.tex` for default packages, as evidenced by the name.

## Import Order
To avoid errors when designing templates, it is useful to know the order in which the template files are placed.
This is given as follows:
1. `defaults/doctype.tex`
2. `defaults/packages.tex`
3. `defaults/macros.tex`
4. `macros/*` - any macro files included in the template, imported in the same order specified.
5. A space for file-specific macros (user macros are placed here when updating a file).
6. `share/formatting/*.tex`, whatever formatting file you specified
7. A space for the main document (document is placed here when updating).
As a general rule, I try to avoid importing anything in the formatting file to avoid conflict with user imports (notable exception: font packages).

# Using the Module
