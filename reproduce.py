"""Reproduce the ProteinGym DMS-Indels result in seconds — apply ProteinGym's OFFICIAL grouped
aggregation to the bundled per-assay Spearman table. Verifies: consensus 0.5165 == PoET 0.5169 (a tie),
and Progen2-M = 0.465 (scorer validation).

Bundled (small, verifiable):
  - per_assay_spearman.csv : per-assay Spearman of {legal consensus, PoET, Progen2-M} vs DMS_score
  - DMS_indels.csv         : the 66-assay reference (UniProt_ID + functional category)

Full reproduction from raw data: download ProteinGym's public `zero_shot_indels_scores` (per-assay CSVs
with each model's zero-shot scores + DMS_score), rank-average all non-PoET model columns per assay, take
Spearman vs DMS_score -> that reproduces per_assay_spearman.csv. Source: https://proteingym.org
"""
import pandas as pd

ref = pd.read_csv("DMS_indels.csv")[["DMS_id", "UniProt_ID", "coarse_selection_type"]].rename(
    columns={"coarse_selection_type": "Selection Type"})
pa = pd.read_csv("per_assay_spearman.csv")


def grouped_average(col):
    """OFFICIAL: per-assay Spearman -> mean within (UniProt_ID, category) -> mean across UniProts in each
    category -> mean across categories (categories weighted equally)."""
    df = ref.merge(pa[["DMS_id", col]], on="DMS_id").dropna(subset=[col])
    by = df.groupby(["UniProt_ID", "Selection Type"])[col].mean()
    return float(by.groupby("Selection Type").mean().mean())


prog = grouped_average("Progen2_medium_spearman")
cons = grouped_average("consensus_spearman")
poet = grouped_average("PoET_spearman")

print(f"Progen2-M (scorer validation) = {prog:.4f}   (published anchor 0.465, err {abs(prog-0.465):.4f})")
print(f"Legal consensus (no PoET)     = {cons:.4f}")
print(f"PoET (#1)                     = {poet:.4f}")
print(f"margin vs #1                  = {cons-poet:+.4f}  "
      f"(negligible: essentially TIED with #1 — matched, does NOT beat it)")
