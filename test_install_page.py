"""Static release-link contract for the public installation page."""

from pathlib import Path


PAGE = Path(__file__).with_name("index.html").read_text(encoding="utf-8")


def test_page_offers_both_mac_architectures() -> None:
    assert 'data-asset="copier-agent-macos-apple-silicon"' in PAGE
    assert 'data-asset="copier-agent-macos-intel"' in PAGE
    assert "Apple Silicon (M1 or later)" in PAGE
    assert "Intel processor" in PAGE


def test_page_explains_device_code_onboarding() -> None:
    assert "Copy device code" in PAGE
    assert "TV1-" in PAGE


def test_mac_commands_choose_the_download_for_this_cpu() -> None:
    assert 'uname -m' in PAGE
    assert 'copier-agent-macos-apple-silicon' in PAGE
    assert 'copier-agent-macos-intel' in PAGE
    assert '~/Downloads/copier-agent-macos\n' not in PAGE
