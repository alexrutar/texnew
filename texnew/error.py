class TexnewError(Exception):
    pass

class TexnewFileError(TexnewError):
    def __init__(self, filename):
        self.filename = filename
        self.context = "Base"
        self.context_info = {}

    def __str__(self):
        return "[{}]: Missing file/directory at \"{}\"".format(self.context,self.filename)

# catch "IsADirectoryError"
class TexnewInputError(TexnewError):
    def __init__(self, user_input):
        self.user_input = user_input
        self.context = None
