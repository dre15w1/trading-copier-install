"""Static release-link contract for the public installation page."""

from pathlib import Path


PAGE = Path(__file__).with_name("index.html").read_text(encoding="utf-8")


def test_page_offers_apple_silicon_and_a_pinned_legacy_intel_build() -> None:
    # Since v0.15.0 the compiled (Nuitka) "latest" build is Apple-Silicon-only.
    # Rather than leave Intel subscribers with a dead end, the Intel card is
    # pinned to the last Intel-compatible release (v0.14.8) via a direct href
    # plus class="unavailable" (excludes it from the auto-resolve-to-latest
    # loop) rather than a data-asset lookup against the latest release.
    assert 'data-asset="copier-agent-macos-apple-silicon"' in PAGE
    assert 'data-asset="copier-agent-macos-intel"' not in PAGE
    assert "Apple Silicon (M1 or later)" in PAGE
    assert "Intel processor" in PAGE
    assert "releases/download/v0.14.8/copier-agent-macos-intel" in PAGE
    assert "last Intel-compatible build" in PAGE
    assert "Update temporarily unavailable" not in PAGE
    assert 'id="dl-mac-arm" href="#" aria-disabled="true"' not in PAGE
    assert "Download for Apple Silicon" in PAGE
    assert "Download v0.14.8 (legacy)" in PAGE


def test_windows_download_uses_the_friendly_installer() -> None:
    assert 'data-asset="Trading-Copier-Setup.exe"' in PAGE
    assert 'data-asset="copier-agent-windows.exe"' not in PAGE


def test_page_explains_device_code_onboarding() -> None:
    assert "Copy device code" in PAGE
    assert "TV1-" in PAGE
    assert "You never enter or send a signal key" in PAGE
    assert "six setup" not in PAGE


def test_mac_commands_pick_the_right_file_by_chip_architecture() -> None:
    assert 'uname -m' in PAGE
    assert 'copier-agent-macos-apple-silicon' in PAGE
    assert 'copier-agent-macos-intel' in PAGE
    assert 'will not run on it' not in PAGE
    assert '~/Downloads/copier-agent-macos\n' not in PAGE


def test_page_has_all_longterm_provider_and_cost_instructions() -> None:
    for text in ("OpenAI", "Anthropic", "Ollama", "No AI", "charge you directly",
                 "Long Term starts at 0%", "approval queue", "Delete saved key"):
        assert text in PAGE
    assert "openai.com/api/pricing" in PAGE
    assert "docs.anthropic.com/en/docs/about-claude/pricing" in PAGE
    assert "ollama.com/download" in PAGE
