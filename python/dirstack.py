import os

class dirstack:
    stack = []
    def __init__(self):
        pass
    def pushd(self):
        self.stack.append(os.getcwd())
    def popd(self):
        if len(self.stack):
            os.chdir(self.stack.pop())
