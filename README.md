# texnew

## Using this program.
In order to run this, you need some version of python (it definitely works in 3.5, and probably earlier), as well as the `pyyaml`, `argparse` packages. The easiest way to call this at any time is to add something like `alias texnew="python /path/to/texnew/texnew.py"` to your bashrc (or equivalent) and you can call the program globally. Use `texnew -h` for basic usage info.

### Updating your templates
If you've created a template using this program (after March 20, 2019), you can automatically update the template using `texnew -u <file.tex> <template>`. This saves file macros you've defined (under `file-specific macros`), as well as the main contents of your document (after `document start`), and places them in a newly generated template, generated from the updated macro files. Your old file is saved in the same directory.

### Checking your templates
If you made changes to macro files, you can run `texnew -c` to automatically compile your templates and check for LaTeX errors (any error that shows up in your log file). Note that the checker works by making a system call to `latexmk`, so it may not work on your system. It also might not work on Windows no matter what. I'm not sure.

## Roll your own templates
It's pretty easy to make your own templates. Here's the key information about the structure of this program:
1. User Info: `src/user.yaml`, `src/user_private.yaml`
    - Input custom user data here; see Formatting. You can also use `src/user_private.yaml`. The program will default to using this file if possible. If the file does not exist, you will get a warning but the program will still generate a template (without substitutions).

2. Templates: `templates`
    - Define new templates in the existing style. There are three (mandatory) options. `doctype` can be any valid LaTeX document type (e.g. article, book). `formatting` must be any filename (without extension) defined in Formatting. `macros` must be any filename (without extension) defined in Macros.

2. Macros: `src/macros`
    - Macro files stored here are accessed by the `macro` option in the templates. You can add your own macros, or pretty much whatever you want here.

3. Formatting: `src/formatting`
    - Formatting files stored here are accessed by the `formatting` option in the templates. I've generally used them to define formatting for the file appearance (fonts, titlepages, etc). They must include `\begin{document}`. Then `\end{docment}` label is automatically placed afterwards.

    - Wherever `<+key+>` appears in a formatting document, they are automatically replaced by the relevant info in the `user.yaml` file. `key` can be any string. You can define new keys.

4. Defaults: `src/defaults`
    - Default files are loaded every time, regardless of the template used. Don't change the file names or weird things will happen, but feel free to change the defaults to whatever you want. `doctype.tex` must have the document class, and the tag `<+doctype+>` is automatically substituted by the defined value in a template. `macros.tex` is for default macros, and `packages.tex` for default packages, as evidenced by the name.

### Import Order
To avoid errors when designing templates, it is useful to know the order in which the template files are placed.
This is given as follows:
1. `src/defaults/doctype.tex`
2. `src/defaults/packages.tex`
3. `src/defaults/macros.tex`
4. Any macro files included in the template, imported in the same order specified.
5. A space for file-specific macros (user macros are placed here when updating a file).
6. `src/formatting/*.tex`, whatever formatting file you specified
7. A space for the main document (document is placed here when updating).
As a general rule, I try to avoid importing anything in the formatting file (notable exception: font packages).

