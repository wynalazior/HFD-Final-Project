# Strategy1 - Group 2 Notebook: READY FOR EXECUTION ✅

## Overview
Group 2 notebook is fully prepared and verified. All cells point to correct data files and include comprehensive visualizations matching Group 1 work.

## Verification Results

### Data File Configuration ✅
| Section | Verification | Status |
|---------|--------------|--------|
| Cell 2 (Data Loading) | Uses `data2_*.parquet` glob pattern | ✅ CORRECT |
| Cell 7 (Initial Backtest) | Uses `data2_*.parquet` glob pattern | ✅ CORRECT |
| Cell 9 (Grid Search) | TRAIN_TAGS/VAL_TAGS/TEST_TAGS use `data2_*` prefix | ✅ CORRECT |
| Cell 12 (Final Backtest) | Uses optimized params loaded from `data2_*` | ✅ CORRECT |
| Cell 18 (OOS Evaluation) | Uses `DATA_DIR_OOS.glob("data2_*.parquet")` | ✅ CORRECT |

### Visualizations Present ✅
- **Cell 8**: Initial portfolio 3-panel chart (PnL, returns, trades)
- **Cell 14**: Grid search optimization heatmaps
- **Cell 15-16**: Percentage strategy visualizations
- **Cell 17**: Quarterly breakdown analysis
- **Cell 19**: OOS consolidated comparison (ATR vs Percentage by quarter)
- **Cell 20**: Execution verification checklist with status table

### Assets and Configuration ✅
| Parameter | Value |
|-----------|-------|
| Group Assets | CAD, AUD, XAU, XAG |
| Data Frequency | 5-minute bars |
| Trading Hours | 24-hour market with 1-hour break (16:50-18:10 CET) |
| Open Range Window | 18:10-19:10 (first hour after break) |
| No-Trade Zone | 18:00-18:10 |

### Strategy Implementations ✅
1. **ATR-Based ORB** (`run_orb_strategy_group2()`)
   - Used in Cells 8, 12, 18
   - Grid search: 3 ATR windows × 5 multipliers × 4 assets = 60 combinations
   
2. **Percentage-Based ORB** (`run_orb_strategy_percentage()`)
   - Used in Cells 15, 16, 18
   - Improved variant with percentage-based thresholds

## Execution Plan

### Phase 1: Core Setup (Cells 1-6)
- Library imports and function definitions
- No dependencies, safe to run sequentially
- Time: ~1-2 minutes

### Phase 2: Initial Backtest (Cells 7-11)
- Baseline ATR strategy with default parameters
- Portfolio visualization and analysis
- Time: ~5-10 minutes

### Phase 3: Grid Search Optimization (Cells 9-11)
- Parameter tuning across 60 combinations
- Validation analysis
- Time: **15-20 minutes** (longest section)

### Phase 4: Final Backtest (Cells 12-13)
- ATR strategy with optimized parameters
- Train/Val/Test performance comparison
- Time: ~5-10 minutes

### Phase 5: Percentage Strategy (Cells 14-17)
- Percentage-based strategy implementation
- Quarterly breakdown analysis
- Time: ~10-15 minutes

### Phase 6: OOS Evaluation (Cell 18)
- Evaluates both strategies on out-of-sample data
- Filters for `data2_*` files only from `../data_oos/`
- Gracefully handles missing data
- Time: ~5-10 minutes

### Phase 7: Final Analysis (Cells 19-20)
- Consolidated comparison visualization
- Execution verification and summary
- Time: ~2-3 minutes

**Total Estimated Time: 45-75 minutes**

## Required Files

```
Training Data (../data/):
  ✅ data2_2023_Q1.parquet
  ✅ data2_2023_Q3.parquet
  ✅ data2_2023_Q4.parquet
  ✅ data2_2024_Q2.parquet
  ✅ data2_2024_Q4.parquet
  ✅ data2_2025_Q1.parquet
  ✅ data2_2025_Q2.parquet

OOS Data (../data_oos/) - Optional but recommended:
  ✅ data2_2023_Q2.parquet
  ✅ data2_2024_Q1.parquet
  ✅ data2_2024_Q3.parquet
  ✅ data2_2025_Q3.parquet
  ✅ data2_2025_Q4.parquet
```

## Expected Output Directories

```
Testing/
├── outputs_orb_group2/                    ← Initial baseline results
│   ├── orb_summary.csv
│   └── {quarter}_portfolio_daily.csv (7 files)
│
├── outputs_orb_group2_final/              ← Optimized ATR results
│   ├── orb_final_summary.csv
│   ├── tuning_results.csv
│   └── {quarter}_portfolio_daily.csv (7 files)
│
├── outputs_orb_group2_percentage/         ← Percentage strategy results
│   ├── tuning_results_percentage.csv
│   ├── orb_percentage_summary.csv
│   └── {quarter}_portfolio_daily.csv (7 files)
│
├── outputs_orb_group2_oos_final/          ← OOS evaluation (ATR)
│   ├── orb_oos_final_summary.csv
│   └── {quarter}_portfolio_daily.csv (5 files)
│
└── outputs_orb_group2_percentage_oos/    ← OOS evaluation (Percentage)
    ├── orb_pct_oos_final_summary.csv
    ├── oos_netpnl_by_quarter.png
    └── {quarter}_portfolio_daily.csv (5 files)
```

## Key Metrics Computed

For each strategy and quarter:
- **net_cumPnL**: Cumulative net profit/loss
- **netSR**: Net annualized Sharpe ratio (√252)
- **netCR**: Net annualized Calmar ratio
- **netMDD**: Maximum drawdown
- **netWR**: Win rate
- **trades_per_day**: Average trades per trading day
- **stat**: STAT score = (netSR - 0.5) × ln(|netPnL / 1000|)

## Critical Checks Before Execution

- [ ] Python 3.10+ installed with pandas 3.0.0+, numpy 2.4.1+, matplotlib 3.10.8+
- [ ] Working directory is `Testing/` folder
- [ ] `../data/` contains all 7 data2_*.parquet files
- [ ] `../data_oos/` contains OOS data (optional, gracefully handled if missing)
- [ ] Sufficient disk space for output files (~100-200 MB)
- [ ] No data1_*.parquet files in same directories (they will be ignored)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| KeyError on asset name | Check that data2_*.parquet files contain CAD, AUD, XAU, XAG columns |
| Grid search very slow | Normal! 60 combinations × 7 quarters = 420 evaluations. Patience required. |
| Missing OOS data | Cell 18 has try/except - it will skip OOS if files don't exist |
| Out of memory | Reduce grid search parameters or increase available RAM |
| Plot not displaying | Use `%matplotlib inline` if running in Jupyter |

## Success Criteria

✅ **Notebook execution is successful when:**
1. All 20 cells execute without errors
2. At least 3+ output directories created with CSV files
3. Performance metrics printed to console for all strategies
4. Visualizations save to disk as PNG files
5. No KeyError or data mismatch warnings

## Notes

- **Group 1 data protection**: All `data1_*.parquet` files in any directory are automatically ignored by glob patterns
- **OOS flexibility**: If data_oos is empty, Cell 18 gracefully skips to Cell 19
- **Parameter consistency**: All cells use same assets (CAD, AUD, XAU, XAG) - no cross-contamination with Group 1
- **Reproducibility**: Results are deterministic; re-running produces same output (if data unchanged)

## Comparison with Group 1

| Aspect | Group 1 | Group 2 |
|--------|---------|---------|
| Assets | SP, NQ | CAD, AUD, XAU, XAG |
| Frequency | 1-minute bars | 5-minute bars |
| Trading Hours | US equity (09:31-16:00) | 24-hour with break |
| Data File Prefix | `data1_*` | `data2_*` |
| Grid Search Combos | 30 (2 assets × 3×5) | 60 (4 assets × 3×5) |
| Est. Execution | 30-45 min | 45-75 min |

---

**STATUS: ✅ NOTEBOOK IS READY FOR EXECUTION**

No further code changes needed. All cells verified to use correct data files and include necessary visualizations. Ready for independent end-to-end run.
