import time
import random
import argparse
import matplotlib.pyplot as plt

def linear_max(arr, post_iters=0):
    m = max(arr)
    for _ in range(post_iters):
        _ = sum(x * 0.000001 for x in arr)
    return m

def cost_aware_max(arr, threshold=0.5, sample_size=None, known_upper=None, post_iters=0):
    n = len(arr)
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

    for _ in range(post_iters):
        _ = sum(x * 0.000001 for x in candidates)

    return m

def run_benchmark(post_iters=0, sample_size=None, known_upper=None, do_plot=False):
    input_sizes = [2000, 5000, 10000, 20000, 40000]
    linear_times, threshold_times = [], []

    for n in input_sizes:
        arr = [random.randint(1, 1000000) for _ in range(n)]

        t0 = time.time()
        linear_max(arr, post_iters=post_iters)
        t1 = time.time()
        linear_times.append(t1 - t0)

        t0 = time.time()
        cost_aware_max(arr, threshold=0.8, sample_size=sample_size,
                       known_upper=known_upper, post_iters=post_iters)
        t1 = time.time()
        threshold_times.append(t1 - t0)

    for n, lt, tt in zip(input_sizes, linear_times, threshold_times):
        print(f"n={n:6d} | Linear={lt:.6f} sec | Cost-Aware={tt:.6f} sec")

    if do_plot:
        plt.figure(figsize=(8,5))
        plt.plot(input_sizes, linear_times, "o-", label="Linear Max")
        plt.plot(input_sizes, threshold_times, "s-", label="Cost-Aware Max")
        plt.xlabel("Input size (n)")
        plt.ylabel("Execution time (seconds)")
        plt.title("Benchmark: Linear vs Cost-Aware Maximum Finding")
        plt.legend()
        plt.tight_layout()
        plt.savefig("demo_plot.png")
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", action="store_true")
    parser.add_argument("--post-iters", type=int, default=0)
    parser.add_argument("--sample-size", type=int, default=None)
    parser.add_argument("--known-upper", type=int, default=None)
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()

    arr = [random.randint(1, 1000000) for _ in range(10000)]

    if args.compare:
        run_benchmark(post_iters=args.post_iters,
                      sample_size=args.sample_size,
                      known_upper=args.known_upper,
                      do_plot=args.plot)
    else:
        t0 = time.time()
        linear_max(arr, post_iters=args.post_iters)
        t1 = time.time()
        print(f"Linear scan: {t1 - t0:.6f} sec")

        t0 = time.time()
        cost_aware_max(arr, threshold=0.8,
                       sample_size=args.sample_size,
                       known_upper=args.known_upper,
                       post_iters=args.post_iters)
        t1 = time.time()
        print(f"Threshold scan: {t1 - t0:.6f} sec")
