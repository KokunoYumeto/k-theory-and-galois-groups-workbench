# Check of the braid identity used in Remark 5.6 of the note (the route through braid groups):
#     (s_1 s_2 ... s_{n-1})^n  =  (s_1 ... s_{n-2})^{n-1} * (s_{n-1} ... s_2 s_1 s_1 s_2 ... s_{n-1})      in B_n,
# and that the two factors on the right commute.  It is verified for n = 2, ..., 6 in Artin's faithful action of
# B_n on the free group F_n:  s_i : x_i -> x_i x_{i+1} x_i^-1,  x_{i+1} -> x_i,  x_j -> x_j otherwise.
# A braid word is applied letter by letter; two words give the same braid iff they give the same automorphism.
# Free group words are tuples of nonzero integers (k for x_k, -k for x_k^-1), freely reduced.

def reduce(w):
    out = []
    for a in w:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return tuple(out)

def inv(w):
    return tuple(-a for a in reversed(w))

def sigma_images(n, i, sign):
    """images of x_1..x_n under s_i (sign=+1) or its inverse (sign=-1)"""
    img = {k: (k,) for k in range(1, n + 1)}
    if sign > 0:
        img[i] = (i, i + 1, -i)
        img[i + 1] = (i,)
    else:
        img[i] = (i + 1,)
        img[i + 1] = (-(i + 1), i, i + 1)
    return img

def apply_letter(n, aut, i, sign):
    """compose: first the automorphism aut, then the letter (substitute the images of the letter into aut)"""
    img = sigma_images(n, i, sign)
    new = {}
    for k in range(1, n + 1):
        w = []
        for a in aut[k]:
            w.extend(img[a] if a > 0 else inv(img[-a]))
        new[k] = reduce(w)
    return new

def automorphism(n, word):
    aut = {k: (k,) for k in range(1, n + 1)}
    for letter in word:
        aut = apply_letter(n, aut, abs(letter), 1 if letter > 0 else -1)
    return aut

ok = True
# sanity: the braid relation and the far commutation hold in this action, and s_1 s_2 != s_2 s_1
assert automorphism(3, [1, 2, 1]) == automorphism(3, [2, 1, 2])
assert automorphism(4, [1, 3]) == automorphism(4, [3, 1])
assert automorphism(3, [1, 2]) != automorphism(3, [2, 1])
for n in range(2, 7):
    delta_n = list(range(1, n))                      # s_1 ... s_{n-1}
    delta_m = list(range(1, n - 1))                  # s_1 ... s_{n-2}
    y_n = list(range(n - 1, 0, -1)) + list(range(1, n))   # s_{n-1} ... s_1 s_1 ... s_{n-1}
    lhs = automorphism(n, delta_n * n)
    rhs = automorphism(n, delta_m * (n - 1) + y_n)
    rhs2 = automorphism(n, y_n + delta_m * (n - 1))
    # the full twist acts by conjugation by a power of x_1 ... x_n: check that it fixes that product
    prod = []
    for k in range(1, n + 1):
        prod.extend(lhs[k])
    fixes_product = reduce(prod) == tuple(range(1, n + 1))
    good = lhs == rhs and rhs == rhs2 and fixes_product
    ok = ok and good
    print("n = %d: delta_n^n = delta_{n-1}^{n-1} * y_n: %s; the two factors commute: %s; fixes x_1...x_n: %s"
          % (n, lhs == rhs, rhs == rhs2, fixes_product))
print("ALL AS CLAIMED" if ok else "MISMATCH")
