class Complex:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary
    def __add__(self, x):
        return Complex(self.real + x.real, self.imaginary + x.imaginary)
    def __mul__(self, x):
        real = self.real * x.real - self.imaginary * x.imaginary
        imaginary = self.real * x.imaginary + self.imaginary * x.real
        return Complex(real, imaginary)
    def __repr__(self):
        return f'{self.real} + {self.imaginary}j'
