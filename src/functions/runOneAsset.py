import numpy as np, pandas as pd

def run_one_asset(df, price_col):
    CAD = df[price_col].to_numpy()
    n   = len(df)
    if price_col == "CAD":
        TC = 10.0
        POINT_VALUE = 100000.0
    elif price_col =="AUD":
        TC = 10.0
        POINT_VALUE = 100000.0
    elif price_col == "XAU":
        TC = 15.0
        POINT_VALUE = 100.0
    elif price_col == "XAG":
        TC = 10.0
        POINT_VALUE = 5000.0
    else:
        TC = 0  # Default value for other assets
        POINT_VALUE = 1  # Default point value

    MASK_NO_TRADE  = df["mask_no_trade"].to_numpy(dtype=bool)
    MASK_FLAT_FROM = df["mask_flat_from"].to_numpy(dtype=bool)

    ENTRY_CUTOFF = pd.to_datetime("14:30").time()
    MASK_NO_ENTRY_AFTER = (df.index.time >= ENTRY_CUTOFF)

    dS = np.diff(CAD)

    SMA_grid = [100, 150, 180]
    slow_mult_grid = [2.0, 2.5, 3.0]
    slope_m_grid = [3, 4, 5]
    z_entry_grid = [1.6, 1.8, 2.0]
    z_stop_grid  = [2.5, 3.0, 3.5]
    z_sl_grid    = [1.5, 2.0, 2.5]
    z_mom_grid   = [0.3, 0.4, 0.5]
    cooldown_grid = [5]

    best_net_pnl = -np.inf
    best_params  = None

    for SMA_win in SMA_grid:
        SMA = pd.Series(CAD).rolling(SMA_win, min_periods=SMA_win // 2).mean().to_numpy()
        STD = pd.Series(CAD).rolling(SMA_win, min_periods=SMA_win // 2).std().to_numpy()
        z   = (CAD - SMA) / np.where(STD == 0, np.nan, STD)

        for slow_mult in slow_mult_grid:
            SMA_slow_win = int(slow_mult * SMA_win)
            SMA_slow = pd.Series(CAD).rolling(SMA_slow_win, min_periods=SMA_slow_win // 2).mean().to_numpy()

            for slope_m in slope_m_grid:
                for z_entry in z_entry_grid:
                    for z_stop in z_stop_grid:
                        for z_sl in z_sl_grid:
                            for z_mom in z_mom_grid:
                                for cooldown_bars in cooldown_grid:

                                    pos = np.zeros(n, dtype=np.int8)
                                    cooldown = 0

                                    for t in range(1, n):
                                        if MASK_FLAT_FROM[t-1]:
                                            pos[t] = 0
                                            cooldown = 0
                                            continue

                                        if (not np.isfinite(CAD[t-1]) or not np.isfinite(SMA[t-1]) or not np.isfinite(STD[t-1]) or
                                            not np.isfinite(z[t-1])  or not np.isfinite(SMA_slow[t-1])):
                                            pos[t] = pos[t-1]
                                            cooldown = cooldown - 1 if cooldown > 0 else 0
                                            continue

                                        if STD[t-1] <= 0:
                                            pos[t] = pos[t-1]
                                            cooldown = cooldown - 1 if cooldown > 0 else 0
                                            continue

                                        if t >= 2 and CAD[t-1] == CAD[t-2]:
                                            pos[t] = pos[t-1]
                                            cooldown = cooldown - 1 if cooldown > 0 else 0
                                            continue

                                        if t-1-slope_m >= 0 and np.isfinite(SMA_slow[t-1-slope_m]):
                                            slow_up  = SMA_slow[t-1] > SMA_slow[t-1-slope_m]
                                            slow_dn  = SMA_slow[t-1] < SMA_slow[t-1-slope_m]
                                            trend_up = (SMA[t-1] > SMA_slow[t-1]) and slow_up
                                            trend_dn = (SMA[t-1] < SMA_slow[t-1]) and slow_dn
                                        else:
                                            trend_up = False
                                            trend_dn = False

                                        up_confirm = (t >= 2) and (CAD[t-1] > CAD[t-2])
                                        dn_confirm = (t >= 2) and (CAD[t-1] < CAD[t-2])

                                        if t >= 3 and np.isfinite(z[t-2]):
                                            z_up_mom = (z[t-1] >= z[t-2] + z_mom)
                                            z_dn_mom = (z[t-1] <= z[t-2] - z_mom)
                                        else:
                                            z_up_mom = False
                                            z_dn_mom = False

                                        if MASK_NO_TRADE[t-1] and pos[t-1] == 0:
                                            pos[t] = 0
                                            cooldown = cooldown - 1 if cooldown > 0 else 0
                                            continue

                                        if MASK_NO_ENTRY_AFTER[t-1] and pos[t-1] == 0:
                                            pos[t] = 0
                                            cooldown = cooldown - 1 if cooldown > 0 else 0
                                            continue

                                        if pos[t-1] == 0:
                                            if cooldown > 0:
                                                pos[t] = 0
                                            else:
                                                if (trend_up and up_confirm and z_up_mom and (z[t-1] >= z_entry) and (z[t-1] <= z_stop)):
                                                    pos[t] = 1
                                                elif (trend_dn and dn_confirm and z_dn_mom and (z[t-1] <= -z_entry) and (z[t-1] >= -z_stop)):
                                                    pos[t] = -1
                                                else:
                                                    pos[t] = 0

                                        elif pos[t-1] == 1:
                                            if (z[t-1] <= -z_sl) or (trend_dn and z[t-1] < 0.0) or (z[t-1] <= -z_stop):
                                                pos[t] = 0
                                                cooldown = cooldown_bars
                                            else:
                                                pos[t] = 1

                                        else:
                                            if (z[t-1] >= z_sl) or (trend_up and z[t-1] > 0.0) or (z[t-1] >= z_stop):
                                                pos[t] = 0
                                                cooldown = cooldown_bars
                                            else:
                                                pos[t] = -1

                                        cooldown = cooldown - 1 if cooldown > 0 else 0

                                    trades  = np.abs(np.diff(pos))
                                    r_net   = POINT_VALUE * (pos[:-1] * dS) - TC * trades
                                    net_pnl = np.nansum(r_net)

                                    if net_pnl > best_net_pnl:
                                        best_net_pnl = net_pnl
                                        best_params  = (SMA_win, slow_mult, slope_m, z_entry, z_stop, z_sl, z_mom, cooldown_bars)

    return best_net_pnl, best_params
