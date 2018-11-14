from functools import wraps

class whenthen:
    def __init__(self):
        self.order = True

    def when(self, func):
        if self.order:
            pass
        else:
            raise AttributeError("then is needed")

    def then(self, func):
        pass


def main():
    pass

if __name__ == '__main__':
    main()
