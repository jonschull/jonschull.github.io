
### error box for print()
class MyOutput:
    def __init__(self):
        self.console = document["console"]
    def write(self, text):
        self.console.html +=  text + '</hr>'
