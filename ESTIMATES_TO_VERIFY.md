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
