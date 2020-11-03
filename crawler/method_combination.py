class MethodCombination:

    def __init__(self, methods=[]):
        self.methods = methods

    def append_method(self,method):
        self.methods.append(method)

    def get_name(self):
        str = ""
        for method in self.methods:
            str += f"{method[0]}-"
        return str
