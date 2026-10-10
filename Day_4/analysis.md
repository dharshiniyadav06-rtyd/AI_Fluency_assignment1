# Day 4 — Will It Fit, and May I Use It?

## Scenario

I want to run a local AI college assistant on my Windows laptop for personal study and coding help. The laptop has 15.8 GB of system RAM. My estimator reserves 30% of RAM for Windows and other applications, giving an available model-memory budget of approximately 11.1 GB. No dedicated GPU VRAM was detected, so the scenario uses CPU inference / shared integrated graphics memory.

The purpose of this analysis is to estimate whether different open models can fit on my laptop and to understand how model size, quantization and context length affect memory usage. I will also check model licences before deciding whether a model can be used.

---

# 3.1 Explanation of Concepts

## 1. Model Weights

Model weights are the numerical values learned during model training. The amount of memory required for the weights mainly depends on the number of model parameters and the number of bytes used to represent each parameter.

The basic estimate is:

**Weights = Number of parameters × Bytes per parameter**

For example, for an 8B model using Q4_K_M:

**8B × 0.57 bytes/parameter = 4.56 GB**

Therefore, the estimated weight memory is 4.56 GB.

Weights are important for the **fit decision** because a model with more parameters generally requires more memory. If the weights alone are too large, the model may not fit within the available memory.

If the weight requirement is ignored, I could select a model that cannot run on my laptop. The limitation in my scenario is that my safe memory budget is only 11.1 GB, so larger models such as the 30B and 70B examples exceed the available memory.

---

## 2. Quantization

Quantization reduces the number of bits or bytes used to represent model values. This reduces the memory required by the model.

In my estimator, different quantization levels have different bytes-per-parameter values. For the same 8B model at an 8K context, the estimated total memory was:

| Quantization |  Weights | KV Cache |    Total | Fits 11.1 GB?  |
| ------------ | -------: | -------: | -------: | -------------- |
| Q3_K_M       |  3.44 GB |  1.28 GB |  5.19 GB | Yes            |
| Q4_K_M       |  4.56 GB |  1.28 GB |  6.42 GB | Yes            |
| Q5_K_M       |  5.44 GB |  1.28 GB |  7.39 GB | Yes            |
| Q8_0         |  8.00 GB |  1.28 GB | 10.21 GB | Yes, but tight |
| FP16         | 16.00 GB |  1.28 GB | 19.01 GB | No             |

This shows that lower-bit quantization reduces the weight memory and therefore the total memory requirement.

Quantization is useful for the **fit decision**, but it can involve a trade-off in model quality. If I use very low precision only to save memory, some quality may be lost compared with higher precision.

For my scenario, Q4_K_M provides a useful balance because the 8B model requires 6.42 GB in the estimator and fits comfortably within the 11.1 GB budget.

---

## 3. KV Cache and Context Length

The KV cache is memory used by the model during inference to keep information from the current context. Context length is the amount of information the model can process at one time.

In my experiment, I kept the model at 8B parameters and Q4_K_M quantization while changing the context length.

| Context | Weights | KV Cache |    Total | Fits?          |
| ------: | ------: | -------: | -------: | -------------- |
|      4K | 4.56 GB |  0.64 GB |  5.72 GB | Yes            |
|      8K | 4.56 GB |  1.28 GB |  6.42 GB | Yes            |
|     32K | 4.56 GB |  5.12 GB | 10.65 GB | Yes, but tight |
|    128K | 4.56 GB | 20.48 GB | 27.54 GB | No             |

The important observation is that the **weights remain fixed at 4.56 GB**, while the KV cache increases as the context length increases.

This means that a model that fits at a short context can stop fitting at a longer context. This is particularly important for an AI agent because an agent may keep adding conversation history and tool results to its context.

In my scenario, 32K was the largest tested context that fitted within the 11.1 GB budget, although it was tight. At 128K, the estimated total increased to 27.54 GB and did not fit.

---

## 4. Model Card

A model card is the documentation provided for an AI model. It can contain information such as the model's publisher, parameter size, intended uses, limitations, licence, supported capabilities and other technical information.

I would use the model card before downloading a model to check whether it is suitable for my scenario. The model card is important for both the technical and permission decisions.

If I ignore the model card, I may misunderstand the model's capabilities, limitations or licence. For example, a model may be technically small enough to run on my laptop but still have licence conditions that affect how I can use or distribute it.

---

## 5. Open-Weight vs Open-Source Licensing

Open-weight means that the trained model weights are available to download and run. Open-weight does not automatically mean that the model has an unrestricted open-source licence.

The exact licence determines what users are allowed to do, including possible conditions on commercial use, redistribution or other uses.

Therefore, memory is not the only factor in choosing a model. A model may fit my laptop but still not be suitable for a particular project if its licence does not permit the intended use.

For my personal study scenario, I will still check the exact licence before selecting a model. For a commercial or public application, licence conditions would become especially important.

---

# 3.2 Memory Estimate Table

My available model-memory budget is **11.1 GB**.

| Model              | Params (B) | Precision | Context (K) | Weights (GB) | KV Cache (GB) | Total (GB) | Fits in 11.1 GB? |
| ------------------ | ---------: | --------- | ----------: | -----------: | ------------: | ---------: | ---------------- |
| Qwen small         |        1.5 | Q4_K_M    |           8 |         0.85 |          0.24 |       1.20 | Yes              |
| Granite / Qwen mid |        8.0 | Q4_K_M    |           8 |         4.56 |          1.28 |       6.42 | Yes              |
| Mid at FP16        |        8.0 | FP16      |           8 |        16.00 |          1.28 |      19.01 | No               |
| Large local        |       30.0 | Q4_K_M    |           8 |        17.10 |          4.80 |      24.09 | No               |

The table shows that the 1.5B Q4_K_M and 8B Q4_K_M configurations fit within my 11.1 GB budget. The 8B FP16 and 30B Q4_K_M configurations do not fit.

The estimate is intended to make a practical fit decision before downloading a model. It is an estimate rather than a prediction of exact memory usage to the megabyte because real memory usage can vary with model architecture, runtime settings and implementation.

---

# 3.3 Context Length and Quantization Observation

## Context Length Experiment

I selected the 8B Q4_K_M configuration and changed only the context length.

| Setting changed | Value used | Weights (GB) | KV Cache (GB) | Total (GB) | Fits?          |
| --------------- | ---------: | -----------: | ------------: | ---------: | -------------- |
| Context length  |         4K |         4.56 |          0.64 |       5.72 | Yes            |
| Context length  |         8K |         4.56 |          1.28 |       6.42 | Yes            |
| Context length  |        32K |         4.56 |          5.12 |      10.65 | Yes, but tight |
| Context length  |       128K |         4.56 |         20.48 |      27.54 | No             |

When the context length increased, the weight memory did not change. The KV cache increased, causing the total memory requirement to increase.

The largest tested context that fits within my 11.1 GB budget at Q4_K_M is **32K**, although it is close to the available limit.

---

## Quantization Experiment

I kept the 8B model and 8K context fixed and changed the quantization.

| Setting changed | Value used | Weights (GB) | KV Cache (GB) | Total (GB) | Fits?          |
| --------------- | ---------- | -----------: | ------------: | ---------: | -------------- |
| Quantization    | Q3_K_M     |         3.44 |          1.28 |       5.19 | Yes            |
| Quantization    | Q4_K_M     |         4.56 |          1.28 |       6.42 | Yes            |
| Quantization    | Q5_K_M     |         5.44 |          1.28 |       7.39 | Yes            |
| Quantization    | Q8_0       |         8.00 |          1.28 |      10.21 | Yes, but tight |
| Quantization    | FP16       |        16.00 |          1.28 |      19.01 | No             |

When quantization changed, the **weight memory changed**, while the KV cache remained 1.28 GB in this estimator.

For my scenario, I would choose **Q4_K_M** for the 8B model. It requires 6.42 GB in the estimate and leaves a reasonable amount of the 11.1 GB budget available for the operating system and other applications. Choosing Q4 instead of higher precision gives up some numerical precision and potentially some model quality, but it provides a much more practical memory requirement for my laptop.

Overall, the experiments show that **quantization mainly changes the weight memory, while context length mainly changes the KV cache memory**.
