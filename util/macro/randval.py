import numpy as np
import random
import time


def getNumpyRandNorm():
    mean = 2
    std_dev = 0.01
    # num_samples = 5

    samples = np.random.normal(mean, std_dev, size=1)
    # for x in samples:
    #     print(f"Generated value: {x:.3f}")
    return samples[0]

def tick(mu, sigma=.001):
    print(mu,sigma, random.gauss(mu=mu, sigma=sigma))
    # time.sleep(random.gauss(mu=mu, sigma=sigma))

if __name__ == "__main__":
    for i in range(10):
        tick(.019, .0001)
