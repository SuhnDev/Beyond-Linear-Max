import random, time
import matplotlib.pyplot as plt

def linear_scan(arr):
    start = time.time()
    maximum = max(arr)
    end = time.time()
    return maximum, end - start

def threshold_scan(arr, threshold_ratio=0.8):
    start = time.time()
    upper_bound = max(arr)
    threshold = upper_bound * threshold_ratio
    candidates = [x for x in arr if x >= threshold]
    maximum = max(candidates)
    end = time.time()
    return maximum, end - start, len(candidates)

if __name__ == "__main__":
    sizes = [2_000, 5_000, 10_000, 20_000, 50_000, 100_000]
    linear_times, threshold_times, survivors = [], [], []

    for n in sizes:
        data = [random.randint(1, 10**6) for _ in range(n)]
        _, t_lin = linear_scan(data)
        _, t_thr, s = threshold_scan(data, threshold_ratio=0.8)
        linear_times.append(t_lin)
        threshold_times.append(t_thr)
        survivors.append(s)
        print(f"n={n}: linear={t_lin:.6f}s, cost-aware={t_thr:.6f}s, survivors={s}")

    plt.figure(figsize=(7,5))
    plt.plot(sizes, linear_times, marker="o", label="Linear Max")
    plt.plot(sizes, threshold_times, marker="s", label="Cost-Aware Max (threshold=0.8·max)")
    plt.xlabel("Input size (n)")
    plt.ylabel("Execution time (seconds)")
    plt.title("Benchmark: Linear vs Cost-Aware Maximum Finding")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("benchmark.png")
    print("Saved: benchmark.png")
