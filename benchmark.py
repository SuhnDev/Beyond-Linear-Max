import random, time
import matplotlib.pyplot as plt

def heavy_postprocess(x, iters=1500):
    # CPU-bound dummy work to emulate expensive step (e.g., model inference)
    v = x
    for _ in range(iters):
        v = (v * 1664525 + 1013904223) % 2**32
    return v

def linear_scan(arr):
    start = time.time()
    _ = max(arr)
    end = time.time()
    return end - start

def cost_aware_scan(arr, threshold_ratio=0.8):
    start = time.time()
    upper = max(arr)
    thr = upper * threshold_ratio
    candidates = [x for x in arr if x >= thr]
    end = time.time()
    return end - start, len(candidates)

def linear_with_post(arr, post_iters=1500):
    start = time.time()
    _ = max(arr)
    for x in arr:
        heavy_postprocess(x, iters=post_iters)
    end = time.time()
    return end - start

def cost_aware_with_post(arr, threshold_ratio=0.8, post_iters=1500):
    start = time.time()
    upper = max(arr)
    thr = upper * threshold_ratio
    candidates = [x for x in arr if x >= thr]
    for x in candidates:
        heavy_postprocess(x, iters=post_iters)
    end = time.time()
    return end - start, len(candidates)

if __name__ == "__main__":
    sizes = [2_000, 5_000, 10_000, 20_000, 40_000]
    lin_times, ca_times = [], []
    linp_times, cap_times = [], []

    for n in sizes:
        data = [random.randint(1, 10**6) for _ in range(n)]
        t_lin = linear_scan(data)
        t_ca, s1 = cost_aware_scan(data, threshold_ratio=0.8)
        t_linp = linear_with_post(data, post_iters=1500)
        t_cap, s2 = cost_aware_with_post(data, threshold_ratio=0.8, post_iters=1500)

        lin_times.append(t_lin); ca_times.append(t_ca)
        linp_times.append(t_linp); cap_times.append(t_cap)
        print(f"n={n}: no-post linear={t_lin:.6f}s, cost-aware={t_ca:.6f}s | with-post linear={t_linp:.3f}s, cost-aware={t_cap:.3f}s")

    # Plot 1: no post-processing
    plt.figure(figsize=(7,5))
    plt.plot(sizes, lin_times, marker='o', label='Linear Max (no post-processing)')
    plt.plot(sizes, ca_times, marker='s', label='Cost-Aware (no post-processing)')
    plt.xlabel('Input size (n)')
    plt.ylabel('Execution time (seconds)')
    plt.title('Timing without Post-Processing')
    plt.legend(); plt.grid(True); plt.tight_layout()
    plt.savefig('benchmark_no_post.png')

    # Plot 2: with heavy post-processing
    plt.figure(figsize=(7,5))
    plt.plot(sizes, linp_times, marker='o', label='Linear Max (with heavy post-processing)')
    plt.plot(sizes, cap_times, marker='s', label='Cost-Aware (with heavy post-processing)')
    plt.xlabel('Input size (n)')
    plt.ylabel('Execution time (seconds)')
    plt.title('Timing with Heavy Post-Processing (threshold=0.8·max)')
    plt.legend(); plt.grid(True); plt.tight_layout()
    plt.savefig('benchmark_with_post.png')

    print('Saved: benchmark_no_post.png, benchmark_with_post.png')
