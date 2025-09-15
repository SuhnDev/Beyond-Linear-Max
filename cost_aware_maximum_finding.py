import random
import time

def linear_scan(arr):
    start = time.time()
    maximum = max(arr)
    end = time.time()
    return maximum, end - start

def threshold_scan(arr, threshold_ratio=0.5):
    start = time.time()
    upper_bound = max(arr)
    threshold = upper_bound * threshold_ratio
    candidates = [x for x in arr if x >= threshold]
    maximum = max(candidates)
    end = time.time()
    return maximum, end - start

if __name__ == "__main__":
    data = [random.randint(1, 10**6) for _ in range(10**6)]
    
    max1, t1 = linear_scan(data)
    max2, t2 = threshold_scan(data)
    
    print(f"Linear scan: {t1:.6f} sec")
    print(f"Threshold scan: {t2:.6f} sec")
