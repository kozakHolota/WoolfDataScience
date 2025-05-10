from sympy import *


x = symbols('x')
x0=0
print("lim (n -> 0) sin(x)/x = ", limit(sin(x)/x, x, x0))
print("lim (n -> 0) tan(x)/x = ", limit(tan(x)/x, x, x0))
print("lim (n -> 0) arctan(x)/x = ", limit(atan(x)/x, x, x0))
print("lim (n -> 0) arcsin(x)/x = ", limit(asin(x)/x, x, x0))
print("lim (n -> 0) (1 - cos(x))/x**2/2 = ", limit((1-cos(x))/(x**2/2), x, x0))