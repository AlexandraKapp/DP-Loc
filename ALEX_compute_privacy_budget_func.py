# compute privacy budget eps


import tensorflow_privacy

from tensorflow_privacy.privacy.analysis import compute_dp_sgd_privacy

n = 50000
noise_multiplier = 0.3
batch_size = 200
epochs = 15
delta = 1 / n

compute_dp_sgd_privacy.compute_dp_sgd_privacy(
        n, batch_size, noise_multiplier, epochs, delta)