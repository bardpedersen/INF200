

class ComplexNumber:
    def __init__(self, a=0, b=0):
        """
        :param a:
        is the real part of the complex number
        :param b:
        is the imaginary part of the complex number
        """
        self.re = a
        self.im = b

    def __str__(self):
        return f'{self.re} + {self.im}j'

    def __repr__(self):
        return f'ComplexNumber({self.re,self.im})'

    def __add__(self, other):
        if type(other) is int or type(other) is float:
            other = ComplexNumber(other)
            return ComplexNumber(self.re + other.re, self.im + other.im)
        else:

            return ComplexNumber(self.re + other.re, self.im + other.im)

    def __sub__(self, other):
        if type(other) is int or type(other) is float:
            other = ComplexNumber(other)
            return ComplexNumber(self.re - other.re, self.im - other.im)
        else:
            return ComplexNumber(self.re - other.re, self.im - other.im)

    def __mul__(self, other):
        try:
            cNUm = ComplexNumber(self.re * other.re - self.im * other.im, self.im * other.re + self.re * other.re)
        except AttributeError:
            other = ComplexNumber(other)
            cNUm = ComplexNumber(self.re * other.re - self.im * other.im, self.re * other.re + self.re * other.re)
        return cNUm

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        try:
            r = float(other.re ** 2 + other.im ** 2)
            cNum = ComplexNumber((self.re * other.re + self.im * other.im) / r, (self.im * other.re - self.re * other.im) / r)
        except AttributeError:
            other = ComplexNumber(other)
            r = float(other.re ** 2 + other.im ** 2)
            cNum = ComplexNumber((self.re * other.re + self.im * other.im) / r, (self.im * other.re - self.re * other.im) / r)
        return cNum

    def __eq__(self, other):
        if self.re == other.re and self.im == other.im:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.re != other.re or self.im != other.im:
            return True
        elif self.re != other.re and self.im != other.im:
            return True
        else:
            return False
