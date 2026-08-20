from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
PDF = ROOT / "Trading-Copier-Setup-Guide.pdf"


def test_manual_is_detailed_and_current():
    reader = PdfReader(PDF)
    assert len(reader.pages) >= 55
    # Pin the published version; update on every manual publish. (This was
    # stale at v0.13.7 while the repo served the 0.14.8 manual - the pin
    # only works if publishing and updating it travel together.)
    assert "v0.15.2" in str(reader.metadata.title)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    required = [
        "Install on Windows",
        "Install on a Mac",
        "The five setup screens",
        "Schwab portal - create the developer account",
        "Wait for approval, then find the App Key and Secret",
        "Put the Schwab credentials into the copier",
        "Schwab key problems and safe fixes",
        "Trading basics for a first-time investor",
        "Approvals screen",
        "Short Term screen",
        "Long Term overview",
        "Opening Range Breakout",
        "Gamma Level Reaction",
        "Sector rotation",
        "Troubleshooting",
        "Glossary",
        "Authoritative investor references",
        "Live View",
        "Take Profit",
    ]
    for phrase in required:
        assert phrase.lower() in text.lower(), phrase


def test_manual_has_current_screens_and_all_strategy_images():
    screens = list((ROOT / "manual-assets").glob("screen-*.jpg"))
    strategies = list((ROOT / "manual-assets" / "strategies").glob("*.png"))
    assert len(screens) >= 8
    assert len(strategies) == 17
    assert all(path.stat().st_size > 10_000 for path in screens + strategies)
