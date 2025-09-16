#!/usr/bin/env python3
"""
Cost-Aware Maximum Finding (CLI)
- Optional heavy post-processing on candidates only
- Optional sample-based upper-bound estimation (to avoid a full first pass)
"""

import argparse
import random
from time import perf_counter

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


# ---------- Core utilities ----------

def heavy_postprocess(x: int, iters: int = 1500) -> int:
    """CPU-bound dummy work to simulate an expensive step (e.g., model inference)."""
    v = x
    for _ in range(iters):
        v = (v * 1664525 + 1013904223) % (2**32)
    return v


def linear_scan(arr):
    """One-pass max (baseline). Returns (max_value, elapsed_seconds)."""
    t0 = perf_counter()
    m = max(arr)
    t1 = perf_counter()
    return m, (t1 - t0)


def estimate_upper_bound_by_sample(arr, sample_size: int):
    """Return an upper-bound estimate using a uniform random sample."""
    if sample_size <= 0 or sample_size >= len(arr):
        return max(arr)
    sample = random.sample(arr, sample_size)
    return max(sample)


def cost_aware_max(
    arr,
    threshold_ratio: float = 0.8,
    post_iters: int = 0,
    known_upper: int | None = None,
    sample_size: int = 0,
):
    """
    Cost-aware maximum finding.
    - If known_upper is provided, use it.
    - Else if sample_size > 0, estimate upper bound from a sample.
    - Else compute exact upper bound by a full pass (max(arr)).
    - Filter to candidates >= threshold; optionally run heavy post-processing
      only on candidates.

    Returns (max_over_candidates, num_candidates, elapsed_seconds).
    """
    t0 = perf_counter()

    # 1) upper bound
    if known_upper is not None:
        upper = known_upper
    elif sample_size > 0:
        upper = estimate_upper_bound_by_sample(arr, sample_size)
    else:
        upper = max(arr)  # full pass

    # 2) filter candidates
    thr = upper * threshold_ratio
    candidates = [x for x in arr if x >= thr]

    # 3) optional heavy post-processing on candidates only
    if post_iters > 0:
        for x in candidates:
            heavy_postprocess(x, iters=post_iters)

    # 4) compute max among candidates (if any)
    m = max(candidates) if candidates else None

    t1 = perf_counter()
    return m, len(candidates), (t1 - t0)


# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser(
        description="Cost-Aware Maximum Finding with optional post-processing and sample-based upper bound."
    )
    ap.add_argument("--n", type=int, default=50_000, help="input size")
    ap.add_argument("--seed", type=int, default=42, help="random seed")
    ap.add_argument("--threshold", type=float, default=0.8,
                    help="threshold ratio relative to upper bound (0<r<=1)")
    ap.add_argument("--post-iters", type=int, default=0,
                    help="simulate heavy post-processing per candidate (0=off)")
    ap.add_argument("--known-upper", type=int, default=None,
                    help="known upper bound for the data (skip first full pass)")
    ap.add_argument("--sample-size", type=int, default=0,
                    help="if >0, estimate upper bound from a random sample of this size")
    ap.add_argument("--compare", action="store_true",
                    help="also run baseline linear scan and print both")
    ap.add_argument("--plot", action="store_true",
                    help="plot time vs n (requires matplotlib)")
    ap.add_argument("--max-n", type=int, default=200_000,
                    help="largest n when using --plot")
    args = ap.parse_args()

    random.seed(args.seed)

    # Generate synthetic data
    data = [random.randint(1, 10**6) for _ in range(args.n)]

    # Baseline
    if args.compare:
        base_max, base_t = linear_scan(data)
    else:
        base_max, base_t = None, None

    # Cost-aware
    ca_max, k, ca_t = cost_aware_max(
        data,
        threshold_ratio=args.threshold,
        post_iters=args.post_iters,
        known_upper=args.known_upper,
        sample_size=args.sample_size,
    )

    print(f"\n[Single run]")
    print(f" n={args.n:,}, threshold={args.threshold}, post-iters={args.post_iters}, "
          f"known-upper={args.known_upper}, sample-size={args.sample_size}")
    if args.compare:
        print(f" Linear max:     {base_t:.6f}s")
    print(f" Cost-Aware max:  {ca_t:.6f}s  (candidates={k})")
    if args.compare and ca_max is not None and base_max is not None:
        print(f" max values — linear={base_max}, cost-aware={ca_max}")

    # Optional plotting across sizes
    if args.plot:
        if plt is None:
            print("Matplotlib not available. Install it or remove --plot.")
            return
        sizes = [2_000, 5_000, 10_000, 20_000, 50_000, 100_000, args.max_n]
        sizes = sorted(set(s for s in sizes if s is not None and s > 0))
        lin_ts, ca_ts = [], []
        for n in sizes:
            data = [random.randint(1, 10**6) for _ in range(n)]
            if args.compare:
                _, t_lin = linear_scan(data)
                lin_ts.append(t_lin)
            m, k, t_ca = cost_aware_max(
                data,
                threshold_ratio=args.threshold,
                post_iters=args.post_iters,
                known_upper=args.known_upper,
                sample_size=args.sample_size,
            )
            ca_ts.append(t_ca)

        import matplotlib.ticker as mticker
        plt.figure(figsize=(7, 5))
        if args.compare:
            plt.plot(sizes, lin_ts, marker="o", label="Linear")
        label = "Cost-Aware"
        if args.post_iters > 0:
            label += f" (post={args.post_iters})"
        if args.known_upper is not None:
            label += ", known-upper"
        elif args.sample_size > 0:
            label += f", sample={args.sample_size}"
        else:
            label += ", full-pass upper"
        plt.plot(sizes, ca_ts, marker="s", label=label)
        plt.xlabel("Input size (n)")
        plt.ylabel("Time (s)")
        plt.title("Linear vs Cost-Aware Maximum Finding")
        plt.grid(True)
        plt.legend()
        plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.3f'))
        out = "demo_plot.png"
        plt.tight_layout()
        plt.savefig(out)
        print(f"Saved plot: {out}")


if __name__ == "__main__":
    main()
