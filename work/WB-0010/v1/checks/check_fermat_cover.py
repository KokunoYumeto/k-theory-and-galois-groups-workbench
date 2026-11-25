# Check of the homological fact used in the proof of Theorem A(b) for the pair of pants (Section 2 of the note).
#
# G = F(x,y) is the fundamental group of a wedge of two circles (homotopy equivalent to the pair of pants),
# z = (xy)^-1, and U_0 is the kernel of G -> (Z/p)^2, x -> (1,0), y -> (0,1).  The cover of the wedge with group
# U_0 is the Cayley graph of (Z/p)^2: vertices (i,j), an x-edge (i,j) -> (i+1,j), a y-edge (i,j) -> (i,j+1).
# H_1 of this graph is U_0^ab = H_1(S';Z), S' the cover of the pair of pants.
#
# The boundary components of S' are the closed walks x^p, y^p, z^p from the vertices: p of each kind.
# Claims checked for p = 2, 3, 5, 7:
#  (1) each of these walks is closed and the 3p edge vectors span a lattice of rank 3p - 1;
#  (2) their sum is zero, so the only relation is the sum of all of them;
#  (3) hence for any three components b1 (over x), b2 (over y), b3 (over z): b1 + b2 + b3 != 0 when 3p > 3.
# Exact arithmetic with Python integers (fraction-free elimination).
from fractions import Fraction
from itertools import product

def rank(rows):
    m = [[Fraction(v) for v in r] for r in rows]
    rk = 0
    ncols = len(m[0]) if m else 0
    for c in range(ncols):
        piv = None
        for r in range(rk, len(m)):
            if m[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        for r in range(len(m)):
            if r != rk and m[r][c] != 0:
                t = m[r][c] / m[rk][c]
                m[r] = [a - t * b for a, b in zip(m[r], m[rk])]
        rk += 1
    return rk

def check(p):
    V = [(i, j) for i in range(p) for j in range(p)]
    ex = {(i, j): k for k, (i, j) in enumerate(V)}                 # x-edge leaving (i,j)
    ey = {(i, j): len(V) + k for k, (i, j) in enumerate(V)}        # y-edge leaving (i,j)
    E = 2 * len(V)

    def walk(word, start):
        """word: list of (letter, sign); returns (edge vector, end vertex)."""
        vec = [0] * E
        i, j = start
        for letter, s in word:
            if letter == 'x':
                if s > 0:
                    vec[ex[(i, j)]] += 1; i = (i + 1) % p
                else:
                    i = (i - 1) % p; vec[ex[(i, j)]] -= 1
            else:
                if s > 0:
                    vec[ey[(i, j)]] += 1; j = (j + 1) % p
                else:
                    j = (j - 1) % p; vec[ey[(i, j)]] -= 1
        return vec, (i, j)

    X = [('x', 1)] * p
    Y = [('y', 1)] * p
    Z = [('y', -1), ('x', -1)] * p        # z = (xy)^-1 = y^-1 x^-1, repeated p times
    comps = {}
    for name, word in (('x', X), ('y', Y), ('z', Z)):
        seen = {}
        for v in V:
            vec, end = walk(word, v)
            assert end == v, "walk not closed"
            seen[tuple(vec)] = True
        comps[name] = [list(t) for t in seen]
        assert len(comps[name]) == p, (name, len(comps[name]))
    allc = comps['x'] + comps['y'] + comps['z']
    total = [sum(col) for col in zip(*allc)]
    rk = rank(allc)
    triples_nonzero = all(any(a + b + c != 0 for a, b, c in zip(b1, b2, b3))
                          for b1, b2, b3 in product(comps['x'], comps['y'], comps['z']))
    cyc_rank = E - len(V) + 1
    print("p = %d: boundary components %d, rank of their span %d (= 3p-1: %s), sum of all is zero: %s, "
          "H_1 has rank %d, every b1+b2+b3 nonzero: %s"
          % (p, len(allc), rk, rk == 3 * p - 1, all(t == 0 for t in total), cyc_rank, triples_nonzero))
    return rk == 3 * p - 1 and all(t == 0 for t in total) and (triples_nonzero or p == 1)

res = [check(p) for p in (2, 3, 5, 7)]
print("ALL AS CLAIMED" if all(res) else "MISMATCH")
