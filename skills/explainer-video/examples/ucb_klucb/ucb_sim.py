"""UCB 動画の比較用：1 人のバンディットで UCB1・KL-UCB（c = 0）・Thompson Sampling の後悔を比べる。"""
import numpy as np


def kl_vec(p, q):
    p = np.clip(p, 1e-12, 1 - 1e-12); q = np.clip(q, 1e-12, 1 - 1e-12)
    return p * np.log(p / q) + (1 - p) * np.log((1 - p) / (1 - q))


def klucb_vec(mean, n, f, iters=25):
    lo, hi = mean.copy(), np.ones_like(mean)
    for _ in range(iters):
        mid = (lo + hi) / 2
        ok = n * kl_vec(mean, mid) <= f
        lo = np.where(ok, mid, lo); hi = np.where(ok, hi, mid)
    return lo


def simulate(mu, T, runs, seed=0, samples=200):
    mu = np.asarray(mu, float); K = len(mu)
    rng = np.random.default_rng(seed)
    times = np.unique(np.geomspace(1, T, samples).astype(int))
    out = {}
    for pol in ("ucb1", "klucb", "ts"):
        N = np.zeros((runs, K)); S = np.zeros((runs, K))
        reg = np.zeros(runs); curve = []
        r = np.random.default_rng(seed)
        for t in range(1, T + 1):
            if t <= K:
                a = np.full(runs, t - 1)
            elif pol == "ucb1":
                a = np.argmax(S / N + np.sqrt(2 * np.log(t) / N), axis=1)
            elif pol == "klucb":
                a = np.argmax(klucb_vec(S / N, N, np.log(t)), axis=1)
            else:
                a = np.argmax(r.beta(1 + S, 1 + N - S), axis=1)
            x = (r.random(runs) < mu[a]).astype(float)
            N[np.arange(runs), a] += 1; S[np.arange(runs), a] += x
            reg += mu.max() - mu[a]
            if t in set(times):
                curve.append(reg.mean())
        out[pol] = dict(times=times, curve=np.array(curve), final=reg.copy(), pulls=N.mean(0))
    return out


if __name__ == "__main__":
    import time, pickle
    res = {}
    for name, mu in (("low", [0.10, 0.05, 0.02]), ("mid", [0.60, 0.50, 0.40])):
        t0 = time.time()
        res[name] = simulate(mu, 10_000, 100, seed=1)
        for p, d in res[name].items():
            print(name, p, "regret %.1f ± %.1f" % (d["final"].mean(), 1.96 * d["final"].std() / 10), "pulls", np.round(d["pulls"], 0))
        print("  %.0f s" % (time.time() - t0))
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
    os.makedirs(out, exist_ok=True)
    pickle.dump(res, open(os.path.join(out, "ucb_sim.pkl"), "wb"))
