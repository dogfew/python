value = int(input())
def f(x):
	global value
	while x < value:
		return x + x / f(x+1)
	else:
		return x
e = 2 + 1 / f(1)
print(e)

