# Beyond Linear Max
### Cost-Aware Maximum Finding

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Made with Python](https://img.shields.io/badge/Python-3.x-blue)

This repository explores a threshold-based approach to maximum finding.  
While the theoretical lower bound for maximum search remains **Θ(n)**,  
we investigate whether **cost-aware filtering** can reduce *practical runtime*  
in scenarios where post-processing of candidate elements is expensive.

---

## 🔍 Idea
- Standard maximum finding requires scanning all elements → Θ(n).
- Our approach introduces a **threshold filter**:
  1. Estimate an upper bound for the maximum.
  2. Discard elements below a threshold (e.g., 50% of the bound or a learned quantile).
  3. Only apply expensive post-processing to the reduced candidate set.
- This does **not** improve worst-case complexity, but can reduce the number of expensive operations in practical settings.
👉 *We don’t beat Θ(n), but we save cost when post-processing is expensive.*

---

## 📊 Applications
- Information retrieval (reduce re-ranking candidates)
- Machine learning (filtering before heavy model inference)
- Database queries (avoiding expensive lookups on low-value rows)
- Financial/streaming systems (focus on top signals only)

---

## ⚙️ Example Code
Run the provided Python file:

```bash
python cost_aware_maximum_finding.py
```

➡️ Full code is available here: [cost_aware_maximum_finding.py](./cost_aware_maximum_finding.py)


**Example output:**
```text
Linear scan: 0.012 sec
Threshold scan: 0.007 sec
```

*(Times depend on data distribution and threshold choice.)*

---

## 🚀 Run in Colab
You can try the code directly in Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SuhnDev/Beyond-Linear-Max/blob/main/notebooks/demo.ipynb)

- **Heavy Post-Processing Simulation**  
  Use `--post-iters <k>` to simulate expensive work (e.g., DB lookups, model inference).  
  Cost-Aware will apply this step **only to filtered candidates**, while the baseline applies it to all.

- **Sample-Based Upper Bound Estimation**  
  Use `--sample-size <m>` to estimate an upper bound from a random sample.  
  This avoids a full initial pass but may underestimate.

- **Known Upper Bound**  
  If you already know the dataset's max possible value, pass `--known-upper` to skip the first scan.

### Examples

```bash
# Baseline vs cost-aware (no post-processing)
python cost_aware_maximum_finding.py --compare

# With heavy post-processing, only candidates are expensive
python cost_aware_maximum_finding.py --post-iters 1500 --compare

# Use a known upper bound (fastest)
python cost_aware_maximum_finding.py --known-upper 1000000 --post-iters 1500 --compare

# Estimate upper bound from a sample
python cost_aware_maximum_finding.py --sample-size 1000 --post-iters 1500 --compare

# Plot runtime scaling with n
python cost_aware_maximum_finding.py --post-iters 1500 --sample-size 1000 --compare --plot
```
---

## 📈 Performance Comparison

We provide two complementary plots:

1. **Without post-processing** — both Linear and Cost-Aware runs in **Ω(n)** time,
but Cost-Aware includes an extra filtering step, so the constant factor is larger.
   
   ![no-post](./benchmark_no_post.png)

2. **With heavy post-processing** — both methods still require **O(n)** to scan the input, but Cost-Aware applies the expensive step (e.g., DB lookups / model inference) only to a reduced subset **O(k)** (k ≪ n), instead of **O(n)** in the Linear case. This makes Cost-Aware significantly faster in scenarios where post-processing dominates runtime.
   
   ![with-post](./benchmark_with_post.png)

To reproduce:

```bash
pip install -r requirements.txt
python benchmark.py
```

---

## 🛠️ Tech
- Python 3
- Matplotlib (for plotting)

---

## 📌 Notes
- This is a **prototype** and not an optimized production algorithm.
- The goal is to demonstrate that **cost-aware strategies** can sometimes outperform naive linear scans in practice when post-processing dominates.
  
- Although this repository demonstrates maximum finding, the same cost-aware filtering idea applies to minimum finding as well.
Simply invert the logic (use a lower threshold instead of an upper bound).

In both cases, the theoretical bound remains Θ(n), but practical savings arise when post-processing is costly.

---

## 📫 Contact
Maintained by **SuDev**
feel free to open an issue or suggestion!

---

## 🇰🇷
이 프로젝트는 **후처리 비용이 큰 환경**에서 
임계값 기반 필터링을 활용해 
후보 개수를 줄여 실행 시간을 절감할 수 있는 
실험적 알고리즘 접근을 다룹니다.
