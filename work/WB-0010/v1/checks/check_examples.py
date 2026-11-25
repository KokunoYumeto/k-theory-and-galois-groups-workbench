# Checks for Section 4 of the note (duality alone does not give invertibility).
#
# Example A: lambda = 1, f = [x,y] = x y x^-1 y^-1; quotient A_4, x -> (123), y -> (124).
#   Claim: [x,y] -> (12)(34), f^-1 y f -> (132) = x^-1, so <x, f^-1 y f> has order 3 and <x,y> = A_4 has order 12.
# Example B: lambda = 1, f = [x,y]^2; quotient S_3, x -> (12), y -> (13).
#   Claim: f^-1 y f -> (12) = x, so <x, f^-1 y f> has order 2 and <x,y> = S_3 has order 6.
# Example C (the one of the run LM4_SUCCESSOR): f = [x,y]^2; quotient A_5, x -> (123), y -> (345): image of order 12.
# Relation (I), f(x,y) f(y,x) = 1, holds identically for f = [x,y]^k because [y,x] = [x,y]^-1; it is also tested.
#
# Both conventions for the product of permutations are run: 'rl' (p*q means q first) and 'lr' (p first).

def make_ops(n, conv):
    ident = tuple(range(n))
    if conv == 'rl':
        def mul(p, q):
            return tuple(p[q[i]] for i in range(n))
    else:
        def mul(p, q):
            return tuple(q[p[i]] for i in range(n))
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

def perm(n, *cycles):
    p = list(range(n))
    for c in cycles:
        for i, a in enumerate(c):
            p[a - 1] = c[(i + 1) % len(c)] - 1
    return tuple(p)

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

def run(name, n, x, y, k, conv):
    ident, mul, inv, gen = make_ops(n, conv)
    def comm(a, b):
        return mul(mul(a, b), mul(inv(a), inv(b)))
    def fk(a, b):
        c = comm(a, b); r = ident
        for _ in range(k):
            r = mul(r, c)
        return r
    f = fk(x, y)
    y2 = mul(mul(inv(f), y), f)
    G = gen([x, y]); H = gen([x, y2])
    rel1 = mul(fk(x, y), fk(y, x)) == ident
    print("%s [%s]: |<x,y>| = %d, f = %s, f^-1 y f = %s, |<x, f^-1 y f>| = %d, relation (I): %s"
          % (name, conv, len(G), cyc_str(f), cyc_str(y2), len(H), rel1))
    return len(G), len(H), rel1

ok = True
for conv in ('rl', 'lr'):
    a = run("Example A, f=[x,y],   A_4", 4, perm(4, (1, 2, 3)), perm(4, (1, 2, 4)), 1, conv)
    b = run("Example B, f=[x,y]^2, S_3", 3, perm(3, (1, 2)), perm(3, (1, 3)), 2, conv)
    c = run("Example C, f=[x,y]^2, A_5", 5, perm(5, (1, 2, 3)), perm(5, (3, 4, 5)), 2, conv)
    ok = ok and a == (12, 3, True) and b == (6, 2, True) and c == (60, 12, True)
print("ALL AS CLAIMED" if ok else "MISMATCH")
