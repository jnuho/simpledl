import numpy as np
import random


def getNumpyRandNorm():
    mean = 2
    std_dev = 0.01
    # num_samples = 5

    samples = np.random.normal(mean, std_dev, size=1)
    # for x in samples:
    #     print(f"Generated value: {x:.3f}")
    return samples[0]


if __name__ == "__main__":
    for i in range(10):
        print(random.gauss(mu=.2, sigma=.0005))
