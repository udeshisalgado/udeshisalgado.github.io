"""Regenerate images/location_shift.png used in isf_slides.qmd.

Run from the isf_slides/ folder:  python3 images/make_location_shift.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import lognorm

# Theme colors to match the presentation
color_baseline = "#1A6872"
color_shifted = "#BF505C"
threshold = 14
plt.rcParams['figure.facecolor'] = '#FBFAF4'
plt.rcParams['axes.facecolor'] = '#FBFAF4'

# Baseline LoS distribution (Log-Normal, mean ~8 days)
s, loc, scale = 0.5, 0, 8
x = np.linspace(0, 30, 500)
pdf_baseline = lognorm.pdf(x, s, loc, scale)

# Diagnostic penalty adds a +4 day shift to the location
pdf_shifted = lognorm.pdf(x, s, loc + 4, scale)

prob_baseline = 1 - lognorm.cdf(threshold, s, loc, scale)
prob_shifted = 1 - lognorm.cdf(threshold, s, loc + 4, scale)

plt.figure(figsize=(15, 5), facecolor="#FBFAF4")
ax = plt.gca()
ax.set_facecolor("#FBFAF4")

plt.plot(x, pdf_baseline, color=color_baseline, lw=3,
         label=f'Day 0 Baseline (P > 14: {prob_baseline:.1%})')
plt.fill_between(x, 0, pdf_baseline, where=(x > threshold), color=color_baseline, alpha=0.2)

plt.plot(x, pdf_shifted, color=color_shifted, lw=3, linestyle="--",
         label=f'Updated with Diagnosis (P > 14: {prob_shifted:.1%})')
plt.fill_between(x, 0, pdf_shifted, where=(x > threshold), color=color_shifted, alpha=0.3)

plt.axvline(threshold, color="black", linestyle=":", lw=2)
plt.text(threshold + 0.5, plt.ylim()[1] * 0.6,
         f"Hospital Threshold (e.g., {threshold} days)",
         rotation=0, fontweight="bold", fontsize=16)

plt.title("Location-Shift Model: Impact of Diagnostic Shock on Tail Risk", fontsize=20)
plt.xlabel("Days in Hospital (LoS)", fontsize=16)
plt.ylabel("Probability Density", fontsize=16)
plt.legend(fontsize=16)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("images/location_shift.png", dpi=200, facecolor="#FBFAF4", bbox_inches="tight")
print("saved images/location_shift.png")
