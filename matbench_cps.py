"""MatBench Discovery CPS — reproduce #1's score and show why it's a wall inference-only.
CPS = 0.5*F1 + 0.4*(1 - kappa_SRME/2) + 0.1*(0.15 - RMSD)/0.15   (RMSD term clamped to [0,1]).
Constants verified against the official CPS source (site/src/lib/combined_perf_score.svelte.ts).
Numbers verified against the official model YAMLs (models/*/*.yml)."""

RMSD_BASELINE = 0.15


def cps(f1, kappa, rmsd):
    rterm = max(0.0, min(1.0, (RMSD_BASELINE - rmsd) / RMSD_BASELINE))
    kterm = max(0.0, 1 - kappa / 2)
    return 0.5 * f1 + 0.4 * kterm + 0.1 * rterm


# verified (F1 unique-proto / kappa_SRME / RMSD)
models = {
    "EquFlashV2 (#1)":      (0.929, 0.094, 0.0577),
    "TACE-OAM-RRA (#2)":    (0.928, 0.101, 0.0576),
    "EquiformerV3-OAM (#3)": (0.931, 0.118, 0.0595),
    "PET-OAM-XL (runnable)": (0.924, 0.119, 0.0596),
}
for name, (f1, k, r) in models.items():
    print(f"{name:24s} CPS = {cps(f1, k, r):.4f}")

print("\n--- our achievable ceiling, inference-only ---")
# best case: ensemble F1 ~0.935, but kappa stuck at the best RUNNABLE model's 0.118, RMSD ~0.058
ceiling = cps(0.935, 0.118, 0.058)
print(f"best first-party (F1 0.935 @ runnable kappa 0.118) CPS = {ceiling:.4f}")
print(f"#1 EquFlashV2                                       CPS = {cps(0.929,0.094,0.0577):.4f}")
print(f"=> ceiling {ceiling:.4f} < #1 {cps(0.929,0.094,0.0577):.4f}: NOT beatable inference-only (kappa wall).")
print("Even matching #1's kappa (0.094) with F1 0.924 (PET) only gives "
      f"CPS {cps(0.924,0.094,0.0596):.4f} < 0.907 — F1 too low. The gap is trained-in model quality.")
