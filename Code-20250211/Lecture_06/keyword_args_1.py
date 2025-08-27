# void functions with 6 parameters
def e1(a, b, c, d, e, f):
    # a, b, c, d, e, f are parameters
    print(f"a = {a}, b = {b}, c = {c}, d = {d}, e = {e}, f = {f}")

def main():
    e1(1, 2, 3, 4, 5, 6)
    e1(1, 2, 3, 4, e=5, f=6)       # keyword arguments e, f
    e1(1, 2, c=3, d=4, e=5, f=6)   # keyword arguments c, d, e, f
    e1(1, 2, d=4, e=5, f=6, c=3)   # keyword arguments c, d, e, f
    e1(1, 2, e=5, f=6, c=3, d=4)   # keyword arguments c, d, e, f
    e1(1, 2, d=4, f=6, e=5, c=3)   # keyword arguments c, d, e, f
    e1(1, e=5, f=6, c=3, b=2, d=4) # keyword arguments b, c, d, e, f

main()
