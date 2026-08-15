"""Prepare sanitized screenshots and canonical strategy illustrations.

Run this from the install-site repository after capturing current subscriber
screens into ``.pdf-review/manual-raw``.  Strategy prose and chart geometry are
read from the copier source so the public manual cannot silently invent a
different explanation from the application.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RAW = ROOT / ".pdf-review" / "manual-raw"
OUT = ROOT / "manual-assets"
COPIER_ROOT = Path(r"C:\Projects\trading_bot\.worktrees\trading-copier-device-access")


def _font(size: int, bold: bool = False):
    candidates = [
        Path(r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def _screen(name: str, box: tuple[int, int, int, int], output: str) -> None:
    image = Image.open(RAW / name).convert("RGB")
    image.crop(box).save(OUT / output, quality=92)


def sanitize_screenshots() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Every crop contains only masked or demonstration data.  The Settings
    # connection-code panel is deliberately excluded.
    _screen("home.png", (0, 0, 1265, 1120), "screen-home.jpg")
    _screen("approvals.png", (0, 0, 1265, 792), "screen-approvals.jpg")
    _screen("short-term.png", (0, 0, 1265, 994), "screen-short-term.jpg")
    _screen("long-term.png", (0, 0, 1265, 1320), "screen-long-term-overview.jpg")
    _screen("long-term.png", (0, 1180, 1265, 2500), "screen-long-term-tools.jpg")
    _screen("signal-types.png", (0, 0, 1265, 1500), "screen-signal-types-1.jpg")
    _screen("system-map.png", (0, 0, 1265, 1089), "screen-system-map.jpg")
    _screen("results.png", (0, 0, 1265, 845), "screen-results.jpg")


def _map_y(value: float, low: float, high: float, top: int, bottom: int) -> int:
    return int(bottom - ((value - low) / max(high - low, 1e-9)) * (bottom - top))


def strategy_assets() -> None:
    sys.path.insert(0, str(COPIER_ROOT))
    from copier.shared.strategies import REGISTRY  # noqa: PLC0415
    from copier.shared.strategy_docs import DOCS  # noqa: PLC0415
    from copier.shared.strategy_charts import chart_for  # noqa: PLC0415

    snapshot = []
    chart_dir = OUT / "strategies"
    chart_dir.mkdir(parents=True, exist_ok=True)
    for strategy_id, label in REGISTRY.items():
        doc = DOCS[strategy_id]
        spec = chart_for(strategy_id)
        snapshot.append({"id": strategy_id, "label": label, **doc,
                         "trigger": spec.get("trigger", "") if spec else ""})
        if not spec:
            continue

        width, height = 1100, 560
        image = Image.new("RGB", (width, height), "#0d1117")
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((10, 10, width - 10, height - 10), 22,
                               fill="#161b22", outline="#30363d", width=3)
        draw.text((48, 34), spec["title"], font=_font(30, True), fill="#e6edf3")
        chart_left, chart_right, chart_top, chart_bottom = 55, 865, 105, 500
        bars = spec["bars"]
        values = [v for bar in bars for v in bar] + [spec["entry"], spec["stop"], spec["target"]]
        low, high = min(values), max(values)
        pad = max((high - low) * .12, 1)
        low, high = low - pad, high + pad

        # Guides: boxes and reference lines.
        for guide in spec.get("guides", []):
            kind = guide.get("kind")
            if kind == "line":
                y = _map_y(guide["y"], low, high, chart_top, chart_bottom)
                draw.line((chart_left, y, chart_right, y), fill="#8b949e", width=2)
                draw.text((chart_left + 4, y - 22), guide["label"], font=_font(17), fill="#8b949e")
            elif kind == "box":
                slot = (chart_right - chart_left) / max(len(bars), 1)
                x0 = chart_left + (guide["x0"] + .5) * slot
                x1 = chart_left + (guide["x1"] + .5) * slot
                y0 = _map_y(guide["y1"], low, high, chart_top, chart_bottom)
                y1 = _map_y(guide["y0"], low, high, chart_top, chart_bottom)
                draw.rectangle((x0, y0, x1, y1), outline="#58a6ff", width=2)
                draw.text((x0 + 4, y1 + 4), guide["label"], font=_font(16), fill="#58a6ff")

        slot = (chart_right - chart_left) / max(len(bars), 1)
        candle_w = max(8, int(slot * .48))
        for index, (open_, high_, low_, close) in enumerate(bars):
            x = int(chart_left + (index + .5) * slot)
            color = "#3fb950" if close >= open_ else "#f85149"
            if index < spec.get("entry_at", 0):
                color = "#6e7681"
            draw.line((x, _map_y(high_, low, high, chart_top, chart_bottom),
                       x, _map_y(low_, low, high, chart_top, chart_bottom)), fill=color, width=3)
            top = _map_y(max(open_, close), low, high, chart_top, chart_bottom)
            bottom = _map_y(min(open_, close), low, high, chart_top, chart_bottom)
            draw.rectangle((x - candle_w // 2, top, x + candle_w // 2, max(top + 3, bottom)),
                           fill=color, outline=color)

        for value, label_text, color in ((spec["entry"], "ENTRY", "#58a6ff"),
                                         (spec["stop"], "STOP", "#f85149"),
                                         (spec["target"], "TAKE PROFIT", "#3fb950")):
            y = _map_y(value, low, high, chart_top, chart_bottom)
            draw.line((chart_left, y, chart_right, y), fill=color, width=3)
            draw.text((890, y - 14), label_text, font=_font(20, True), fill=color)

        draw.text((55, 515), "Illustration only - not a prediction or a real trade.",
                  font=_font(17), fill="#9aa5b1")
        image.save(chart_dir / f"{strategy_id}.png")

    (OUT / "strategy-catalogue.json").write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    sanitize_screenshots()
    strategy_assets()
    print(f"Prepared manual assets in {OUT}")
