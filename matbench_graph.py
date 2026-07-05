"""MatBench Discovery kappa_SRME gap: why #1's CPS isn't beatable inference-only. Every open model we can
run has kappa well above #1's 0.094, and kappa is 40% of CPS. Verified numbers from the official model YAMLs."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# kappa_SRME (LOWER is better), verified from official MatBench-Discovery model YAMLs
models = ["EquFlashV2\n(#1)", "EquiformerV3\n-OAM", "PET-OAM-XL\n(runnable)",
          "TACE-OAM-L\n(runnable)", "TACE-v1-OAM-M\n(what we ran)"]
kappa = [0.094, 0.118, 0.119, 0.126, 0.173]
colors = ["#34a853", "#ea8600", "#ea8600", "#ea8600", "#d93025"]

fig, ax = plt.subplots(figsize=(8.5, 5))
bars = ax.bar(models, kappa, color=colors, width=0.62)
for b, k in zip(bars, kappa):
    ax.text(b.get_x() + b.get_width() / 2, k + 0.003, f"{k:.3f}", ha="center", va="bottom",
            fontsize=11, fontweight="bold")
ax.axhline(0.094, ls="--", lw=1.4, color="#34a853")
ax.text(4.35, 0.098, "#1 threshold 0.094", color="#34a853", fontsize=9.5, ha="right")
ax.set_ylabel("κ_SRME  (LOWER = better; 40% of CPS)", fontsize=11)
ax.set_title("MatBench Discovery — the κ wall (why #1's CPS isn't beatable inference-only)\n"
             "Every open model we can run has κ far above #1's 0.094 → CPS ceiling ≈ 0.905 < #1's 0.907",
             fontsize=11)
ax.set_ylim(0, 0.19)
plt.tight_layout()
plt.savefig("matbench-kappa-wall.png", dpi=150)
print("saved matbench-kappa-wall.png")
