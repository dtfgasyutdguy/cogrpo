# -*- coding: utf-8 -*-
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--latent", type=str, required=False, default="mujoco_saved_latent.pkl"
)
# latent = pickle.load(open(args.latent, "rb"))
args = parser.parse_args()



import matplotlib.pyplot as plt

plt.plot(latent)
plt.show()
