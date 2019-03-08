# texnew

## Using this program.
In order to run this, you need some version of python (it definitely works in 3.5, and probably earlier), as well as the `pyyaml`, `argparse` packages. The easiest way to call this at any time is to add something like `alias texnew="python /path/to/texnew/texnew.py"` to your bashrc (or equivalent) and you can call the program globally. Use `texnew -h` for basic usage info.

## Roll your own templates
It's pretty easy to make your own templates. Here's the key information about the structure of this program:
1. User Info: src/user.yaml
    - Input custom user data here; see Formatting

2. Templates: templates
    - Define new templates in the existing style. There are three (mandatory) options. 'doctype' can be any valid LaTeX document type (e.g. article, book). 'formatting' must be any filename (without extension) defined in Formatting. 'macros' must be any filename (without extension) defined in Macros.

2. Macros: src/macros
    - Macro files stored here are accessed by the 'macro' option in the templates. You can add your own macros, or pretty much whatever you want here.

3. Formatting: src/formatting
    - Formatting files stored here are accessed by the 'formatting' option in the templates. I've generally used them to define formatting for the file appearance (fonts, titlepages, etc). They must include '\begin{document}' and '\end{document}'. Whever '<+key+>' appears in a formatting document, they are automatically replaced by the relevant info in the 'user.yaml' file. You can define new keys.
