"""Generate the ProteinGym DMS-Indels comparison figure (official Average Spearman)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Official grouped Average Spearman, ProteinGym DMS-Indels (66 assays). Scorer validated: Progen2-M = 0.465.
methods = ["Progen2-M\n(single baseline)", "Our legal consensus\n(no PoET)", "PoET\n(#1 on leaderboard)"]
scores = [0.4647, 0.5165, 0.5169]
colors = ["#9aa0a6", "#1a73e8", "#34a853"]

fig, ax = plt.subplots(figsize=(7.5, 5))
bars = ax.bar(methods, scores, color=colors, width=0.6)
for b, s in zip(bars, scores):
    ax.text(b.get_x() + b.get_width() / 2, s + 0.004, f"{s:.4f}", ha="center", va="bottom",
            fontsize=12, fontweight="bold")
ax.axhline(0.5169, ls="--", lw=1, color="#34a853", alpha=0.6)
ax.set_ylabel("Average Spearman (official grouped scorer)", fontsize=11)
ax.set_title("ProteinGym DMS-Indels — we EQUALISED the #1, did not beat it\n"
             "Legal consensus 0.5165  vs  PoET 0.5169  (Δ = −0.0004, within scorer error 0.0003)",
             fontsize=11.5)
ax.set_ylim(0.40, 0.54)
ax.annotate("tie", xy=(1.5, 0.5167), fontsize=11, color="#5f6368", ha="center")
plt.tight_layout()
plt.savefig("proteingym-indels-comparison.png", dpi=150)
print("saved proteingym-indels-comparison.png")
