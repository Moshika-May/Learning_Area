def e2(a, b, c, d=4, e=5, f=6):
    # a, b, c, d, e, f are parameters
    # d, e, f have default values
    print(f"a = {a}, b = {b}, c = {c}, d = {d}, e = {e}, f = {f}")

def main():
    e2(1, 2, 3)                    # used default value for d, e, f
    e2(1, 2, 3, 4)                 # used default value for e, f
    e2(1, 2, 3, 4, 5)              # used default value for f
    e2(1, 2, 3, 4, 5, 6)
    e2(1, 2, d=4, e=5, f=6, c=3)   # keyword arguments c, d, e, f
    e2(1, 2, e=5, f=6, c=3, d=4)   # keyword arguments c, d, e, f
    e2(1, 2, d=4, f=6, e=5, c=3)   # keyword arguments c, d, e, f
    e2(1, e=5, f=6, c=3, b=2, d=4) # keyword arguments b, c, d, e, f

main()
