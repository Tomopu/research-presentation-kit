"""動画用の小さな再現：M = K = 2、mu = (0.9, 0.1)。各プレイヤーは自分の観測だけを使い、衝突の 0 も失敗として数える。"""
import math
import numpy as np

MU = np.array([0.9, 0.1])


def kl(p, q):
    p = min(max(p, 1e-12), 1 - 1e-12); q = min(max(q, 1e-12), 1 - 1e-12)
    return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))


def klucb(mean, n, f):
    if n == 0:
        return 1.0
    lo, hi = mean, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        if n * kl(mean, mid) <= f:
            lo = mid
        else:
            hi = mid
    return lo


def run(policy, seed, T=3000, M=2):
    rng = np.random.default_rng(seed)
    K = len(MU)
    N = np.zeros((M, K)); S = np.zeros((M, K))
    choices = np.zeros((T, M), int); coll = np.zeros(T, bool); post = []
    for t in range(1, T + 1):
        a = np.zeros(M, int)
        for m in range(M):
            if policy == "ts":
                v = rng.beta(1 + S[m], 1 + N[m] - S[m])
            else:
                f = math.log(t)
                v = np.array([klucb(S[m, k] / N[m, k] if N[m, k] else 0.0, N[m, k], f) for k in range(K)])
                v = v + 1e-9 * rng.random(K)
            a[m] = int(np.argmax(v))
        x = (rng.random(K) < MU).astype(float)
        c = a[0] == a[1]
        for m in range(M):
            r = 0.0 if c else x[a[m]]
            N[m, a[m]] += 1; S[m, a[m]] += r
        choices[t - 1] = a; coll[t - 1] = c
        post.append((N.copy(), S.copy()))
    return choices, coll, post


if __name__ == "__main__":
    for pol in ("klucb", "ts"):
        stuck = []
        for s in range(40):
            ch, co, _ = run(pol, s, T=2000)
            stuck.append(co[-500:].mean())
        print(pol, np.round(stuck, 2))
