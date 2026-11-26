# Placeholder estimates (shown in RED in the PDF via \est{}). Replace with re-run values, then delete \est{}.

| Where | Cells | How estimated |
|---|---|---|
| tab:summary, Rank column | 3.05 / 7.98 / 7.74 / 4.22 / 6.01 / 4.76 / 5.78 / 2.81 (VolTilt 2.65 kept) | Old ranks of the 8 other methods rescaled by (45-2.65)/(sum of old) so the 9 mean ranks sum to 45.00 (FinMem rounded up 0.01 to hit 45.00) |
| tab:sens, W1 row | all VolTilt cells | Old cell + 0.69 (= new default 2.45 - old default 1.76); EW column untouched; row best re-bolded (0 bps = 2.49) |
| tab:sens, IB crypto row | all VolTilt cells | Old cell + 0.26 (= 1.04 - 0.78); row best re-bolded (window 10 = 1.52) |
| tab:sens, IB stocks row | unchanged | default already 2.39 = tab:main |
| Prose (cost sensitivity sentence) | W1 Sharpe 2.34 to 2.49 across costs | min/max of the estimated W1 cost columns |
| Prose (W1 paired Sharpe gap) | +1.18 CI [+0.71,+1.65] | Gap = 2.45-1.27 (from tables); CI = old half-width (0.465) re-centred on +1.18 |

## Still UNCHANGED but possibly stale (not red)
- tab:summary: Wins (x/13) and Wilcoxon p columns, incl. p=0.520 vs Vol scaling. Kept from the old run.
- tab:w1: Leg wins 4/6.
- Crypto VolTilt (tab:main 1.04, tab:ablation ~1.02) does not equal vol scaling (0.78) although the method says tilt is off for 2 assets.

## Consistency constraints a rerun must satisfy (moved from experiments.tex header, 26 Nov)

```
CONSISTENCY CONSTRAINTS a rerun must satisfy (check these against
new results before they enter the paper):
  C1  Table \ref{tab:main} VolTilt row = Table \ref{tab:ablation}
      VolTilt row (gpt-oss-120b column) = Table \ref{tab:sens}
      Default column, exactly, per benchmark.
  C2  IB crypto (N=2): the rank tilt collapses to the equal-weight
      composition, so VolTilt = portfolio scaling (0.78) for EVERY
      labeller; the rank-tilt ablation row = portfolio scaling;
      tilt-only = equal weight (0.98); the tilt-strength columns of
      Table \ref{tab:sens} equal the default. If a rerun breaks
      this, a new mechanism exists and must be defined and ablated.
  C3  Table \ref{tab:controls} LLM gain == VolTilt - Core for the
      same labeller/benchmark (same smoothed signal and policy).
  C4  Table \ref{tab:matched-budget} diagonal (News,News) ==
      Table \ref{tab:ablation} VolTilt for Qwen3-8B, same settings.
  C5  The 3 bps run freezes holdings and dates of the 5 bps run and
      varies only the cost: SR and CR slightly higher at 3 bps, MDD
      essentially unchanged (no -3.5% vs -12.0% style jumps).
  C6  Mean ranks in Table \ref{tab:summary} sum to 45 over the nine
      methods run on all 13 asset-window entries.
  C7  Paired Sharpe differences are reported against BOTH the
      equal-weight reference and volatility scaling, with CIs.
  C8  Bold = best value per the caption rule of each table; recheck
      bold placement whenever any number changes.

RECONCILIATION DECISIONS (why 1.92 and not 2.45):
  - The shifted-score null 95th percentile is ~+0.20 (Table 5), so a
    tilt gain of +0.67 (implied by W1 = 2.45 over scaling 1.78) is
    implausible; the matched-budget diagonals (+0.09/+0.15) and the
    controls gains (+0.04..+0.32) all support ~+0.1..+0.15.
  - Hence W1 VolTilt = 1.92 (= scaling 1.78 + 0.14), IB stocks
    VolTilt = 2.39 (= Table 1/9 value), crypto = 0.78 (C2).
  - Table \ref{tab:summary} VolTilt Sharpe kept at 1.31 (per-asset
    Sharpe is composition-insensitive; the crypto collapse changes
    it only marginally), but CR/MDD were shifted for the corrected
    crypto panel (+21.8 / -9.5).
```

## Review-guide items (26 Nov) not resolvable by writing
- Block-bootstrap CIs for portfolio Sharpe differences, matched-budget cells and delay (shown as red "pending").
- Cross-sectional IC of smoothed traded score; sentiment-only comparator; gpt-oss-120b 2x2 decomposition; post-cutoff untouched window.
- Ledger-based returns, drift-based costs, average invested fraction and realised volatility (P0 items 01-03).
- Verify ranks, Wilcoxon p-values, wins on regenerated per-asset series.
