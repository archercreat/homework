from functools import wraps

class whenthen:
    def __init__(self, func):
        self._when = False
        self.func = func

    def __call__(self, *args, **kwags):
        pass

    def when(self, func):
        if not self._when:
            # code
            self._when = True
        else:
            raise AttributeError("then is needed")

    def then(self, func):
        # code
        self._when = False


def main():
    @whenthen
    def fract(x):
        return x * fract(x - 1)


    @fract.when
    def fract(x):
        return x == 0


    @fract.then
    def fract(x):
        return 1


    @fract.when
    def fract(x):
        return x > 5


    @fract.then
    def fract(x):
        return x * (x - 1) * (x - 2) * (x - 3) * (x - 4) * fract(x - 5)

    print(fract(0))

if __name__ == '__main__':
    main()
