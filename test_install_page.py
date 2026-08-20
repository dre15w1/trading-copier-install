"""Static release-link contract for the public installation page."""

from pathlib import Path


PAGE = Path(__file__).with_name("index.html").read_text(encoding="utf-8")


def test_page_offers_apple_silicon_and_is_honest_about_intel() -> None:
    # Since v0.15.0 the compiled (Nuitka) build is Apple-Silicon-only. The
    # Intel card stays visible but is a plain explanation, not a download --
    # a dead download link is worse than an honest "ask Andre".
    assert 'data-asset="copier-agent-macos-apple-silicon"' in PAGE
    assert 'data-asset="copier-agent-macos-intel"' not in PAGE
    assert "Apple Silicon (M1 or later)" in PAGE
    assert "Intel processor" in PAGE
    assert "Not supported by this download" in PAGE
    assert "Update temporarily unavailable" not in PAGE
    assert 'id="dl-mac-arm" href="#" aria-disabled="true"' not in PAGE
    assert "Download for Apple Silicon" in PAGE
    assert "Download for Intel Mac" not in PAGE


def test_windows_download_uses_the_friendly_installer() -> None:
    assert 'data-asset="Trading-Copier-Setup.exe"' in PAGE
    assert 'data-asset="copier-agent-windows.exe"' not in PAGE


def test_page_explains_device_code_onboarding() -> None:
    assert "Copy device code" in PAGE
    assert "TV1-" in PAGE
    assert "You never enter or send a signal key" in PAGE
    assert "six setup" not in PAGE


def test_mac_commands_refuse_intel_and_use_the_apple_silicon_file() -> None:
    assert 'uname -m' in PAGE
    assert 'copier-agent-macos-apple-silicon' in PAGE
    assert 'copier-agent-macos-intel' not in PAGE
    assert 'will not run on it' in PAGE
    assert '~/Downloads/copier-agent-macos\n' not in PAGE


def test_page_has_all_longterm_provider_and_cost_instructions() -> None:
    for text in ("OpenAI", "Anthropic", "Ollama", "No AI", "charge you directly",
                 "Long Term starts at 0%", "approval queue", "Delete saved key"):
        assert text in PAGE
    assert "openai.com/api/pricing" in PAGE
    assert "docs.anthropic.com/en/docs/about-claude/pricing" in PAGE
    assert "ollama.com/download" in PAGE
