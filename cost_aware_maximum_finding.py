import time
import random
import argparse
import matplotlib.pyplot as plt

# ---------------------------
# Linear maximum scan
# ---------------------------
def linear_max(arr, post_iters=0):
    m = max(arr)
    # simulate heavy post-processing on all elements
    for _ in range(post_iters):
        _ = sum(x * 0.000001 for x in arr)
    return m

# ---------------------------
# Cost-aware maximum scan
# ---------------------------
def cost_aware_max(arr, threshold=0.5, sample_size=None, known_upper=None, post_iters=0):
    n = len(arr)

    # upper bound estimation
    if known_upper is not None:
        upper_bound = known_upper
    elif sample_size is not None and sample_size < n:
        sample = random.sample(arr, sample_size)
        upper_bound = max(sample)
    else:
        upper_bound = max(arr)

    cutoff = threshold * upper_bound
    candidates = [x for x in arr if x >= cutoff]

    m = max(candidates) if candidates else max(arr)

    # simulate heavy post-processing only on candidates
    for _ in range(post_iters):
        _ = sum(x * 0.000001 for x in candidates)

    return m

# ---------------------------
# Benchmark runner
# ---------------------------
def run_benchmark(compare=False, post_iters=0, sample_size=None, known_upper=None, do_plot=False):
    input_sizes = [2000, 5000, 10000, 20000, 40000]
    linear_times = []
    threshold_times = []

    for n in input_sizes:
        arr = [random.randint(1, 1000000) for _ in range(n)]

        # Linear scan
        t0 = time.time()
        linear_max(arr, post_iters=post_iters)
        t1 = time.time()
        linear_times.append(t1 - t0)

        # Cost-aware scan
        t0 = time.time()
        cost_aware_max(
            arr,
            threshold=0.8,
            sample_size=sample_size,
            known_upper=known_upper,
            post_iters=post_iters,
        )
        t1 = time.time()
        threshold_times.append(t1 - t0)

    # print results
    for n, lt, tt in zip(input_sizes, linear_times, threshold_times):
        print(f"n={n:6d} | Linear={lt:.6f} sec | Cost-Aware={tt:.6f} sec")

    # plot results
    if do_plot:
        plt.figure(figsize=(8,5))
        plt.plot(input_sizes, linear_times, "o-", label="Linear Max")
        plt.plot(input_sizes, threshold_times, "s-", label="Cost-Aware Max")
        plt.xlabel("Input size (n)")
        plt.ylabel("Execution time (seconds)")
        plt.title("Benchmark: Linear vs Cost-Aware Maximum Finding")
        plt.legend()
        plt.tight_layout()
        plt.savefig("demo_plot.png")   # ✅ 저장
        print("Saved plot as demo_plot.png")

# ---------------------------
# CLI entry
# ---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", action="store_true", help="Run benchmark comparison")
    parser.add_argument("--post-iters", type=int, default=0, help="Simulated post-processing iterations")
    parser.add_argument("--sample-size", type=int, default=None, help="Sample size for upper bound estimation")
    parser.add_argument("--known-upper", type=int, default=None, help="Known upper bound value")
    parser.add_argument("--plot", action="store_true", help="Save benchmark plot as PNG")
    args = parser.parse_args()

    arr = [random.randint(1, 1000000) for _ in range(10000)]

    if args.compare:
        run_benchmark(
            compare=True,
            post_iters=args.post_iters,
            sample_size=args.sample_size,
            known_upper=args.known_upper,
            do_plot=args.plot,
        )
    else:
        t0 = time.time()
        lm = linear_max(arr, post_iters=args.post_iters)
        t1 = time.time()
        print(f"Linear scan: {t1 - t0:.6f} sec")

        t0 = time.time()
        cm = cost_aware_max(
            arr,
            threshold=0.8,
            sample_size=args.sample_size,
            known_upper=args.known_upper,
            post_iters=args.post_iters,
        )
        t1 = time.time()
        print(f"Threshold scan: {t1 - t0:.6f} sec")
