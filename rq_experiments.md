# Research questions and required experiments (draft)

Sources: session minh-2 (w2_oss.md, drl_compare.md, 20B/120B runs, 2026-11-17..19), plus reports4/paper_benchmark.md, voltilt4_oss.md, llm_signal_controls.md, filings_signal.md.
Rule for all RQs: windows, assets, seeds, baselines and tests are fixed before running; every run and window is reported (no selection of seeds or windows by outcome).

| RQ | Question | Experiment | Evidence so far | Gap |
|---|---|---|---|---|
| RQ1 | Under the protocols of FinMem/FinCon/TradingGPT, does VolTilt match or beat LLM agents, DRL and rule baselines? | Main table: FINSABER (6 stocks), InvestorBench stocks and crypto; Sharpe/CR/MDD; 5 bps; 3 seeds for stochastic methods; baselines B&H, SMA, MACD, PPO/A2C/DQN, FinMem, FinCon, TradingGPT, AutoRedTrader, FLAG-Trader | W1: v4 1.82 vs FinMem -0.85, FinCon 0.64, TradingGPT 1.54, B&H 1.27, DQN 1.72, AutoRedTrader 2.11 (not significant vs last two). W2 (calm bull): v4 1.01 = B&H 1.02 | FLAG-Trader has no gpt-oss version; TradingGPT/ARK history, NIO, COIN unavailable; only 3 DRL seeds |
| RQ2 | Where does the gain come from: volatility budget or LLM event tilt? | Ablation: B&H, vol scaling only, tilt only, vol+tilt (rank/magnitude); tilt vs shifted-score null and article-count control | Vol-only 1.28 vs v4 1.25 (13 assets, Qwen); tilt gain +0.02..+0.19, null p 0.13-0.54 (Qwen, gpt-oss-20b) | Repeat controls with 120B labels |
| RQ3 | Does LLM-extracted news information predict future returns? | Rank IC (same day, next day, 5 days), cluster bootstrap; 10-K/10-Q filings (Holm) | Same-day IC +0.13 (0.16 with 120B), next/5-day ~0 for all 3 models; filings IC ~0 | Intraday timestamps unavailable (dates only) |
| RQ4 | Are conclusions stable across backbones? | Same pipeline with Qwen3-8B, gpt-oss-20b, gpt-oss-120b | v4 stable (1.25 / 1.26); FinCon 1.20 -> -0.13, FinMem -0.16 -> -0.51 when the backbone changes | 120B: W2 agents running; W1 pending; no GPT-4-class model |
| RQ5 | Is performance stable across market regimes? | Two news windows (W1 2022-10..2023-06, W2 2023-06..2023-12); price-only windows 2020-24 and 2025-26 (news ends 2023) for the LLM-free core | v4 beats B&H in W1 (volatile), ties in W2 (calm); price-only core beats B&H in 2020-24, loses in 2025-26 | More news windows impossible; price-only evidence covers only the risk core |
| RQ6 | Does VolTilt reduce risk at comparable return, and is it cost-robust? | MDD, vol, turnover, cost 0-20 bps, vol target and window sensitivity | MDD -14.3% vs B&H -20.6%, FinCon -18.9%; sensitivity table exists | Report Sharpe, CR and MDD together |
| RQ7 (optional) | Do stronger or memorising LLMs change the answer? | Larger model; look-ahead/memorisation test on pre- vs post-cutoff periods | Not run | Needs a larger model and post-cutoff news |

## Statistical protocol (all RQs)
Block bootstrap CIs on Sharpe differences, Wilcoxon over assets, Holm correction across comparisons, >=5 seeds for stochastic methods, medians reported.

## Honest framing supported by the evidence
VolTilt beats published LLM agents under their own protocols but ties buy-and-hold and vol scaling without LLM in calm windows; the LLM tilt does not separate from null. RQ2/RQ3/RQ4 therefore carry the paper's analytic weight.
