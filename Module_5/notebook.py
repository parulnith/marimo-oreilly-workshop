import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import xarray as xr
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import plotly.express as px
    import plotly.graph_objects as go
    import pystac_client
    import planetary_computer
    import stackstac
    from pathlib import Path
    from concurrent.futures import ThreadPoolExecutor, as_completed

    return (
        Path,
        go,
        mcolors,
        mo,
        np,
        planetary_computer,
        plt,
        px,
        pystac_client,
        stackstac,
    )


@app.cell(hide_code=True)
def _(mo):
    region_picker = mo.ui.dropdown(
        options={
            "Full Thar Desert":         [70.0, 26.5, 73.0, 29.0],
            "Jaisalmer Core":           [69.5, 26.0, 71.5, 27.5],
            "Indira Gandhi Canal Zone": [72.0, 27.5, 74.5, 30.0],
        },
        value="Full Thar Desert",
        label="Region",
    )
    demo_mode = mo.ui.checkbox(label="Demo mode (fast, pre-cached)", value=True)
    run_btn = mo.ui.run_button(label="Load comparison", kind="success")

    mo.vstack([
        mo.md("### Thar Desert Greening: 2018 vs 2022"),
        mo.md("*Comparing monsoon seasons (Jun–Oct) — same months both years, so you see change, not seasonality.*"),
        mo.hstack([region_picker, demo_mode]),
        run_btn,
    ])
    return demo_mode, region_picker, run_btn


@app.cell(hide_code=True)
def _(mo):
    compare_data, set_compare_data = mo.state(None)
    ndvi_state,   set_ndvi_state   = mo.state(None)
    ndvi_cache,   set_ndvi_cache   = mo.state({})
    return (
        compare_data,
        ndvi_cache,
        ndvi_state,
        set_compare_data,
        set_ndvi_cache,
        set_ndvi_state,
    )


@app.cell(hide_code=True)
def _(region_picker):
    bbox = region_picker.value
    return (bbox,)


@app.cell(hide_code=True)
def _(
    Path,
    bbox,
    demo_mode,
    mo,
    ndvi_cache,
    ndvi_state,
    np,
    planetary_computer,
    pystac_client,
    region_picker,
    run_btn,
    set_ndvi_cache,
    set_ndvi_state,
    stackstac,
):
    mo.stop(
        not run_btn.value,
        mo.md("") if ndvi_state() is not None else mo.md("Click **Load comparison** above to fetch Sentinel-2 data."),
    )

    _PERIOD_A_START = "2018-06-01"
    _PERIOD_A_END   = "2018-10-31"
    _CLOUD_MAX      = 20

    _res        = 2000 if demo_mode.value else 1000
    _max_items  = 30   if demo_mode.value else 60
    _max_tiles  = 9    if demo_mode.value else 15
    _bands      = ["B04", "B08"]
    _cache_key  = ("A", _PERIOD_A_START, _PERIOD_A_END, tuple(bbox), demo_mode.value)

    if _cache_key in ndvi_cache():
        _cached = ndvi_cache()[_cache_key]
        set_ndvi_state(_cached)
        mo.stop(True, mo.md(f"⚡ 2018 cached  ·  **{_cached['n_tiles']}** tiles"))

    _region_slug_map = {
        "Full Thar Desert":         "full_thar_desert",
        "Jaisalmer Core":           "jaisalmer_core",
        "Indira Gandhi Canal Zone": "indira_gandhi_canal_zone",
    }
    _region_name = next(
        (k for k, v in region_picker.options.items() if list(v) == list(region_picker.value)),
        "Full Thar Desert",
    )
    _slug = _region_slug_map[_region_name]
    _demo_disk_a = Path(f"demo_cache_{_slug}_2018.npz")
    if demo_mode.value and _demo_disk_a.exists():
        with mo.status.spinner(title=f"⚡ Loading 2018 data for {_region_name}…"):
            _d = np.load(_demo_disk_a)
            _result = {
                "ndvi": _d["ndvi"], "red": _d["red"], "nir": _d["nir"],
                "label": "2018 monsoon",
                "latest": str(_d["latest"]),
                "n_tiles": int(_d["n_tiles"]),
            }
        set_ndvi_state(_result)
        set_ndvi_cache({**ndvi_cache(), _cache_key: _result})
        mo.md(f"⚡ 2018 {_region_name}  ·  **{_result['n_tiles']}** tiles  ·  disk cache")
    else:
        with mo.status.spinner(title="Searching 2018 monsoon..."):
            catalog = pystac_client.Client.open(
                "https://planetarycomputer.microsoft.com/api/stac/v1",
                modifier=planetary_computer.sign_inplace,
            )
            _search = catalog.search(
                collections=["sentinel-2-l2a"],
                bbox=bbox,
                datetime=f"{_PERIOD_A_START}/{_PERIOD_A_END}",
                query={"eo:cloud_cover": {"lt": _CLOUD_MAX}},
                max_items=_max_items,
            )
            all_items = list(_search.items())
            seen_tiles = set()
            items = []
            for _item in sorted(all_items, key=lambda x: x.properties.get("eo:cloud_cover", 99)):
                _tile = _item.properties.get("s2:mgrs_tile", _item.id)
                if _tile not in seen_tiles:
                    seen_tiles.add(_tile)
                    items.append(_item)
            items = items[:_max_tiles]

        mo.stop(len(items) == 0, mo.md("No 2018 scenes found."))

        with mo.status.spinner(title=f"Downloading {len(items)} tiles · 2018 monsoon ({_res} m)…"):
            try:
                _stack = stackstac.stack(items, assets=_bands,
                                         bounds_latlon=bbox, resolution=_res, epsg=32643,
                                         chunksize=2048)
                _data  = _stack.median(dim="time").compute()
            except Exception as _e:
                mo.stop(True, mo.md(f"Download failed. Retry. `{type(_e).__name__}: {_e}`"))

            _red  = _data.sel(band="B04").values.astype(float)
            _nir  = _data.sel(band="B08").values.astype(float)
            _ndvi = np.where((_nir + _red) > 0, (_nir - _red) / (_nir + _red), np.nan)
            _latest = max(items, key=lambda x: x.datetime).datetime.strftime("%Y-%m-%d")

        _result = {
            "ndvi": _ndvi, "red": _red, "nir": _nir,
            "label": "2018 monsoon", "latest": _latest, "n_tiles": len(items),
        }
        set_ndvi_state(_result)
        set_ndvi_cache({**ndvi_cache(), _cache_key: _result})
        mo.md(f"✓ 2018 {_region_name}  ·  **{len(items)}** tiles")
    return


@app.cell(hide_code=True)
def _(
    Path,
    bbox,
    demo_mode,
    mo,
    ndvi_cache,
    ndvi_state,
    np,
    planetary_computer,
    pystac_client,
    region_picker,
    run_btn,
    set_compare_data,
    set_ndvi_cache,
    stackstac,
):
    mo.stop(
        not run_btn.value or ndvi_state() is None,
        mo.md(""),
    )

    _PERIOD_B_START = "2022-06-01"
    _PERIOD_B_END   = "2022-10-31"
    _CLOUD_MAX_B    = 20
    _ndvi_a         = ndvi_state()["ndvi"]
    _res_b          = 2000 if demo_mode.value else 1000
    _max_b          = 30   if demo_mode.value else 60
    _max_tiles_b    = 9    if demo_mode.value else 15
    _cache_k_b      = ("B", _PERIOD_B_START, _PERIOD_B_END, tuple(bbox), demo_mode.value)

    if _cache_k_b in ndvi_cache():
        _cb = ndvi_cache()[_cache_k_b]
        mo.stop(_cb["ndvi"].shape != _ndvi_a.shape,
                mo.md(f"⚠️ Shape mismatch: A={_ndvi_a.shape}, B={_cb['ndvi'].shape}. Clear in-memory cache and reload."))
        set_compare_data({"ndvi_b": _cb["ndvi"], "ndvi_diff": _cb["ndvi"] - _ndvi_a,
                          "label_b": "2022 monsoon", "label_a": "2018 monsoon"})
        mo.stop(True, mo.md(f"⚡ 2022 cached  ·  **{_cb['n_tiles']}** tiles"))

    _region_slug_map_b = {
        "Full Thar Desert":         "full_thar_desert",
        "Jaisalmer Core":           "jaisalmer_core",
        "Indira Gandhi Canal Zone": "indira_gandhi_canal_zone",
    }
    _region_name_b = next(
        (k for k, v in region_picker.options.items() if list(v) == list(region_picker.value)),
        "Full Thar Desert",
    )
    _slug_b = _region_slug_map_b[_region_name_b]
    _demo_disk_b = Path(f"demo_cache_{_slug_b}_2022.npz")
    if demo_mode.value and _demo_disk_b.exists():
        with mo.status.spinner(title=f"⚡ Loading 2022 data for {_region_name_b}…"):
            _db = np.load(_demo_disk_b)
            _result_b = {"ndvi": _db["ndvi"], "n_tiles": int(_db["n_tiles"]),
                         "latest": str(_db["latest"])}
        set_ndvi_cache({**ndvi_cache(), _cache_k_b: _result_b})
        mo.stop(_result_b["ndvi"].shape != _ndvi_a.shape,
                mo.md(f"⚠️ Shape mismatch: A={_ndvi_a.shape}, B={_result_b['ndvi'].shape}. Both periods need matching caches."))
        set_compare_data({"ndvi_b": _result_b["ndvi"], "ndvi_diff": _result_b["ndvi"] - _ndvi_a,
                          "label_b": "2022 monsoon", "label_a": "2018 monsoon"})
        mo.md(f"⚡ 2022 {_region_name_b}  ·  **{_result_b['n_tiles']}** tiles  ·  disk cache")
    else:
        with mo.status.spinner(title="Searching 2022 monsoon..."):
            catalog_b = pystac_client.Client.open(
                "https://planetarycomputer.microsoft.com/api/stac/v1",
                modifier=planetary_computer.sign_inplace,
            )
            _sb = catalog_b.search(
                collections=["sentinel-2-l2a"],
                bbox=bbox,
                datetime=f"{_PERIOD_B_START}/{_PERIOD_B_END}",
                query={"eo:cloud_cover": {"lt": _CLOUD_MAX_B}},
                max_items=_max_b,
            )
            all_items_b = list(_sb.items())
            seen_b = set()
            items_b = []
            for _item in sorted(all_items_b, key=lambda x: x.properties.get("eo:cloud_cover", 99)):
                _tile = _item.properties.get("s2:mgrs_tile", _item.id)
                if _tile not in seen_b:
                    seen_b.add(_tile)
                    items_b.append(_item)
            items_b = items_b[:_max_tiles_b]

        mo.stop(len(items_b) == 0, mo.md("No 2022 scenes found."))

        with mo.status.spinner(title=f"Downloading {len(items_b)} tiles · 2022 monsoon ({_res_b} m)…"):
            _stack_b = stackstac.stack(items_b, assets=["B04", "B08"],
                                       bounds_latlon=bbox, resolution=_res_b, epsg=32643,
                                       chunksize=2048)
            _data_b  = _stack_b.median(dim="time").compute()

        _red_b  = _data_b.sel(band="B04").values.astype(float)
        _nir_b  = _data_b.sel(band="B08").values.astype(float)
        _ndvi_b = np.where((_nir_b + _red_b) > 0, (_nir_b - _red_b) / (_nir_b + _red_b), np.nan)

        _result_b = {"ndvi": _ndvi_b, "n_tiles": len(items_b),
                     "latest": max(items_b, key=lambda x: x.datetime).datetime.strftime("%Y-%m-%d")}
        set_ndvi_cache({**ndvi_cache(), _cache_k_b: _result_b})
        set_compare_data({"ndvi_b": _ndvi_b, "ndvi_diff": _ndvi_b - _ndvi_a,
                          "label_b": "2022 monsoon", "label_a": "2018 monsoon"})
        mo.md(f"✓ 2022 {_region_name_b}  ·  **{len(items_b)}** tiles")
    return


@app.cell(hide_code=True)
def _(compare_data, go, mcolors, mo, ndvi_state, np, plt, px):
    mo.stop(ndvi_state() is None or compare_data() is None,
            mo.md("Click **Load comparison** above to load both 2018 and 2022 imagery."))

    _s     = ndvi_state()
    _cd    = compare_data()
    ndvi_a = _s["ndvi"]
    ndvi_b = _cd["ndvi_b"]
    ndvi_d = _cd["ndvi_diff"]

    def _ndvi_fig(arr, title, vmin=-0.2, vmax=0.6, cbar_title="NDVI"):
        _cmap = plt.colormaps["RdYlGn"].copy()
        _cmap.set_bad("lightgray")
        _rgba = (_cmap(mcolors.Normalize(vmin=vmin, vmax=vmax)(arr)) * 255).astype(np.uint8)
        _fig = px.imshow(_rgba, binary_string=True)
        _fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers", showlegend=False,
            marker=dict(colorscale="RdYlGn", cmin=vmin, cmax=vmax,
                        showscale=True, colorbar=dict(title=cbar_title, tickformat=".2f"),
                        color=[0], opacity=0),
        ))
        _fig.update_layout(title=title, xaxis_title="Column (W→E)", yaxis_title="Row (N→S)",
                           margin=dict(t=50, b=40))
        return _fig

    _mean_a = float(np.nanmean(ndvi_a))
    _mean_b = float(np.nanmean(ndvi_b))
    _delta  = _mean_b - _mean_a
    _greened_pct = float((ndvi_d > 0.05).sum() / np.isfinite(ndvi_d).sum() * 100)

    _summary = mo.md(f"""
    **Mean NDVI**: 2018 = `{_mean_a:.3f}`  →  2022 = `{_mean_b:.3f}`  ·  Δ = `{_delta:+.3f}`  
    **Greened area** (ΔNDVI > 0.05): **{_greened_pct:.1f}%** of valid pixels
    """)

    _cats = ["Bare / desert (< 0.1)", "Sparse veg (0.1–0.3)", "Dense / irrigated (≥ 0.3)"]
    def _shares(arr):
        v = arr[~np.isnan(arr)]
        return [float((v < 0.1).mean()*100),
                float(((v >= 0.1) & (v < 0.3)).mean()*100),
                float((v >= 0.3).mean()*100)]

    _bar = go.Figure()
    _bar.add_trace(go.Bar(name="2018", x=_cats, y=_shares(ndvi_a), marker_color="#a6611a"))
    _bar.add_trace(go.Bar(name="2022", x=_cats, y=_shares(ndvi_b), marker_color="#1a9850"))
    _bar.update_layout(title="Land-cover shares: 2018 vs 2022", barmode="group",
                       yaxis_title="%", margin=dict(t=50, b=40))

    _tabs = mo.ui.tabs({
        "NDVI 2018 (before)":  _ndvi_fig(ndvi_a, "NDVI — 2018 monsoon"),
        "NDVI 2022 (after)":   _ndvi_fig(ndvi_b, "NDVI — 2022 monsoon"),
        "Greening (2022 − 2018)": _ndvi_fig(ndvi_d, "ΔNDVI — Green = greening, Red = drying",
                                             vmin=-0.3, vmax=0.3, cbar_title="ΔNDVI"),
        "Statistics": _bar,
    })

    mo.vstack([_summary, _tabs])
    return


if __name__ == "__main__":
    app.run()
