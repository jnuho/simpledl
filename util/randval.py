import numpy as np


if __name__ == "__main__":
    mean = 2
    std_dev = 0.1
    num_samples = 5

    samples = np.random.normal(mean, std_dev, num_samples)

    for x in samples:
        print(f"Generated value: {x:.3f}")
