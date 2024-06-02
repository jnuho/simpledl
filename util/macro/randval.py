import numpy as np
import random
import time


if __name__ == "__main__":
    mean = 2
    std_dev = 0.1
    num_samples = 5

    samples = np.random.normal(mean, std_dev, num_samples)

    for x in samples:
        print(f"Generated value: {x:.3f}")


def getRand():
    # Define the desired mean (mu) and standard deviation (sigma)
    mu = (0.0183 + 0.0184) / 2
    sigma = (0.0184 - 0.0183) / 6  # Assuming a 6-sigma range for 99.7% coverage

    # Generate a random Gaussian number
    gaussian_number = random.gauss(mu, sigma)

    # Calculate the sleep interval based on the Gaussian number
    interval = abs(gaussian_number)

    # Sleep for the specified interval
    time.sleep(interval)

    print(f"Slept for {interval:.6f} seconds")
