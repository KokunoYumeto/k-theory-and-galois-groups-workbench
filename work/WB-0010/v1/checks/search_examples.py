# Search for small finite quotients in which the substitution x -> x, y -> f^-1 y f is not onto,
# for f = [x,y]^k (k = 1, 2, 3), which satisfies relation (I) f(x,y) f(y,x) = 1 identically.
# Both composition conventions for permutations are tried: 'rl' (p*q = p after q) and 'lr' (p*q = p then q).
# [a,b] = a b a^-1 b^-1 in the chosen convention.
from itertools import permutations

def make_ops(n, conv):
    ident = tuple(range(n))
    def mul_rl(p, q):  # p after q
        return tuple(p[q[i]] for i in range(n))
    def mul_lr(p, q):  # p then q
        return tuple(q[p[i]] for i in range(n))
    mul = mul_rl if conv == 'rl' else mul_lr
    def inv(p):
        r = [0] * n
        for i, v in enumerate(p):
            r[v] = i
        return tuple(r)
    def gen(gens):
        seen = {ident}
        frontier = [ident]
        while frontier:
            nxt = []
            for g in frontier:
                for h in gens:
                    k = mul(h, g)
                    if k not in seen:
                        seen.add(k)
                        nxt.append(k)
            frontier = nxt
        return seen
    return ident, mul, inv, gen

def cyc_str(p):
    n = len(p); seen = set(); out = []
    for i in range(n):
        if i in seen or p[i] == i:
            continue
        c = [i]; seen.add(i); j = p[i]
        while j != i:
            c.append(j); seen.add(j); j = p[j]
        out.append("(" + "".join(str(a + 1) for a in c) + ")")
    return "".join(out) or "()"

def power(mul, ident, a, k):
    r = ident
    for _ in range(k):
        r = mul(r, a)
    return r

def search(n, conv, k, limit=3):
    ident, mul, inv, gen = make_ops(n, conv)
    elems = list(permutations(range(n)))
    found = []
    for x in elems:
        for y in elems:
            G = gen([x, y])
            c = mul(mul(x, y), mul(inv(x), inv(y)))
            f = power(mul, ident, c, k)
            y2 = mul(mul(inv(f), y), f)
            H = gen([x, y2])
            if len(H) < len(G):
                found.append((len(G), len(H), cyc_str(x), cyc_str(y), cyc_str(f), cyc_str(y2)))
    found.sort()
    return found[:limit], len(found)

for conv in ('rl', 'lr'):
    for k in (1, 2, 3):
        for n in (3, 4, 5):
            ex, cnt = search(n, conv, k)
            print("convention", conv, " f=[x,y]^%d" % k, " S_%d:" % n, cnt, "pairs (x,y) with a proper image; smallest:", ex[:2])

# the example of the note, in both conventions
for conv in ('rl', 'lr'):
    ident, mul, inv, gen = make_ops(5, conv)
    x = (1, 2, 0, 3, 4)       # (123)
    y = (0, 1, 3, 4, 2)       # (345)
    c = mul(mul(x, y), mul(inv(x), inv(y)))
    f = mul(c, c)
    y2 = mul(mul(inv(f), y), f)
    print("note example, convention", conv, ": |<x,y>| =", len(gen([x, y])), " f =", cyc_str(f), " f^-1 y f =", cyc_str(y2),
          " |<x, f^-1 y f>| =", len(gen([x, y2])))
