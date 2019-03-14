# take input file
# separate input file into:
# - file macros
# - main files
# merge macros + main file with new template
# copy file to new location
# write new version of file

def l(start):
    return lambda x:x.startswith(start)

def update_file(filename):
    with open(filename,'r') as f:
        macros = separate_file(fl,l("\n% " + "file-specific macros"),l("\n% " + "formatting"))
        body = separate_file(fl,l("\\chapter"),lambda x:False)
