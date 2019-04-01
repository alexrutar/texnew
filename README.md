# Basic Usage
## Using this program.
You can install this command line tool - as well as the module - with `pip install texnew`.
Make sure your `pip` version is for Python 3 (it may be installed under `pip3`).
If you call the command line version, `texnew` looks for template information at `~/.texnew/`.
You should also install the included templates there, which you can find at [texnew-templates](https://github.com/alexrutar/texnew-templates); installation instructions are on that page.
Run `texnew -h` for basic information about the script.

### Update an existing file.
If you've created a template using this program with `texnew` version at least 1.0, you can automatically update the template using `texnew -u <file.tex> <template>`.
This saves file macros you've defined (under `file-specific macros`), as well as the main contents of your document (after `document start`), and places them in a newly generated template, generated from the updated macro files.
Your old file is saved in the same directory with `_old` appended to the name.

### Checking your templates
If you made changes to macro files, you can run `texnew -c` to automatically compile your templates and check for LaTeX errors (any error that shows up in your log file).
Note that the checker works by making a system call to `latexmk`, so it may not work on your system.
It also might not work on Windows no matter what.
I'm not sure.

### Including user info
User info files can be found at `user.yaml`, `user_private.yaml`.

You can input custom information here to be automatically added to templates whenever you generate them; see Formatting below for more detail.
You can also use `user_private.yaml`, the program will prioritize (if it exists).
If neither user file exists, you will get a warning but the program will still generate a template (without substitutions).

# Roll your own templates
Templates are organized into template sets.
If you want to make your own template set, it's recommended to copy the structure in `base`.
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
