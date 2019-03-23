# texnew

## Using this program.
You can install this command line tool - as well as the module - with `pip install texnew`.
If you call the command line version, `texnew` looks for template information at `~/.texnew/` under a specific folder structure.
You should also install the included templates there, which you can find at [texnew-templates](https://github.com/alexrutar/texnew-templates).
Run `texnew -h` for basic information about the script.

### Updating your templates
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

## Roll your own templates
It's pretty easy to make your own templates.
Here's the key information about the structure of this program:

1. Templates: `share/templates`
    - Define new templates in the existing style. There are three (mandatory) options. `doctype` can be any valid LaTeX document type (e.g. article, book). `formatting` must be any filename (without extension) defined in Formatting. `macros` must be any filename (without extension) defined in Macros.

2. Macros: `share/macros`
    - Macro files stored here are accessed by the `macro` option in the templates. You can add your own macros, or pretty much whatever you want here.

3. Formatting: `share/formatting`
    - Formatting files stored here are accessed by the `formatting` option in the templates. I've generally used them to define formatting for the file appearance (fonts, titlepages, etc). They must include `\begin{document}`. Then `\end{docment}` label is automatically placed afterwards.
    - Wherever `<+key+>` appears in a formatting document, they are automatically replaced by the relevant info in the `user.yaml` file. `key` can be any string. You can define new keys.

4. Defaults: `share/defaults`
    - Default files are loaded every time, regardless of the template used. Don't change the file names or weird things will happen, but feel free to change the defaults to whatever you want. `doctype.tex` must have the document class, and the tag `<+doctype+>` is automatically substituted by the defined value in a template. `macros.tex` is for default macros, and `packages.tex` for default packages, as evidenced by the name.

### Import Order
To avoid errors when designing templates, it is useful to know the order in which the template files are placed.
This is given as follows:
1. `share/defaults/doctype.tex`
2. `share/defaults/packages.tex`
3. `share/defaults/macros.tex`
4. Any macro files included in the template, imported in the same order specified.
5. A space for file-specific macros (user macros are placed here when updating a file).
6. `share/formatting/*.tex`, whatever formatting file you specified
7. A space for the main document (document is placed here when updating).
As a general rule, I try to avoid importing anything in the formatting file to avoid conflict with user imports (notable exception: font packages).
