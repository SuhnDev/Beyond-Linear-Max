import random
import time

def linear_scan(arr):
    return max(arr)

def threshold_scan(arr, threshold):
    candidates = [x for x in arr if x >= threshold]
    return max(candidates) if candidates else None

if __name__ == "__main__":
    data = [random.randint(1, 1000) for _ in range(100000)]
    t0 = time.time()
    linear_scan(data)
    t1 = time.time()
    threshold_scan(data, 500)
    t2 = time.time()
    print("Linear scan:", t1 - t0, "sec")
    print("Threshold scan:", t2 - t1, "sec")
    