"""Compatibility entry point for the detailed Trading Copier user manual."""

# Existing release notes and operator habits invoke this filename.  Keep it as
# the stable command while the detailed manual lives in a focused module.
if __name__ == "__main__":
    import build_user_manual  # noqa: F401  (import performs the documented build)
    raise SystemExit(0)

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Trading-Copier-Setup-Guide.pdf"
BLUE = colors.HexColor("#58a6ff")
NAVY = colors.HexColor("#0d1117")
PANEL = colors.HexColor("#161b22")
PANEL2 = colors.HexColor("#1c2128")
INK = colors.HexColor("#e6edf3")
MUTED = colors.HexColor("#9aa5b1")
LINE = colors.HexColor("#30363d")
RED = colors.HexColor("#ff7b72")
GREEN = colors.HexColor("#3fb950")


class GuideDoc(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(filename, pagesize=letter, rightMargin=54, leftMargin=54,
                         topMargin=58, bottomMargin=52,
                         title="Trading Copier - Setup and Use Guide v0.13.7",
                         author="Walkers Software LLC")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
                      id="normal")
        self.addPageTemplates(PageTemplate(id="guide", frames=[frame],
                                           onPage=self._decorate))

    def _decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        canvas.setStrokeColor(LINE)
        canvas.line(54, 40, letter[0] - 54, 40)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(54, 27, "TEAM VILLAIN  /  Trading Copier v0.13.7")
        canvas.drawRightString(letter[0] - 54, 27, f"Page {doc.page}")
        canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
                          fontSize=28, leading=33, textColor=colors.white,
                          alignment=TA_CENTER, spaceAfter=14))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=13,
                          leading=19, textColor=colors.HexColor("#d8edf6"),
                          alignment=TA_CENTER))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold",
                          fontSize=21, leading=25, textColor=INK, spaceAfter=12,
                          keepWithNext=True))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold",
                          fontSize=14, leading=18, textColor=BLUE,
                          spaceBefore=13, spaceAfter=7, keepWithNext=True))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="Helvetica",
                          fontSize=10.2, leading=15, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontSize=8.7,
                          leading=12, textColor=MUTED, spaceAfter=5))
styles.add(ParagraphStyle(name="Codex", parent=styles["Code"], fontName="Courier",
                          fontSize=8.3, leading=12, textColor=INK, backColor=PANEL2,
                          borderPadding=8, borderColor=LINE,
                          borderWidth=0.5, borderRadius=4, spaceBefore=5, spaceAfter=9))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontSize=10,
                          leading=14, textColor=INK, backColor=PANEL2, borderColor=BLUE,
                          borderWidth=1, borderPadding=10, spaceBefore=7, spaceAfter=10))
styles.add(ParagraphStyle(name="Danger", parent=styles["BodyText"], fontSize=10,
                          leading=14, textColor=RED, backColor=colors.HexColor("#2a1315"),
                          borderColor=RED, borderWidth=1,
                          borderPadding=10, spaceBefore=7, spaceAfter=10))


def p(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def bullets(items):
    return ListFlowable([ListItem(p(x), leftIndent=12) for x in items], bulletType="bullet",
                        leftIndent=20, bulletFontName="Helvetica", bulletFontSize=8,
                        bulletColor=BLUE,
                        spaceAfter=8)


def numbered(items):
    return ListFlowable([ListItem(p(x), leftIndent=12) for x in items], bulletType="1",
                        start="1", leftIndent=24, bulletFontName="Helvetica-Bold",
                        bulletColor=BLUE,
                        spaceAfter=8)


def heading(title, kicker=None):
    out = []
    if kicker:
        out.append(p(kicker.upper(), "Smallx"))
    out.append(p(title, "H1x"))
    return out


story = []

# Cover — use the same approved hero and dark interface treatment as the app.
hero = Image(str(ROOT / "tv-hero.jpg"), width=7.0 * inch, height=3.94 * inch)
hero.hAlign = "CENTER"
cover = Table([[
    [hero, Spacer(1, 0.32 * inch), p("Trading Copier", "CoverTitle"),
     p("Setup and Use Guide", "CoverTitle"), Spacer(1, 0.08 * inch),
     p("Version 0.13.7  /  Windows + macOS", "CoverSub"),
     p("Revised 14 August 2026", "CoverSub")]
]], colWidths=[letter[0] - 108], rowHeights=[6.75 * inch])
cover.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                           ("BOX", (0, 0), (-1, -1), 1, LINE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0)]))
story += [cover, PageBreak()]

story += heading("Read this first", "Section 1")
story += [p("The Trading Copier receives encrypted trade signals from Andre and prepares the corresponding order in your own Schwab account. By default, every entry waits for you to approve it. Exits are handled automatically so an open copied position is not abandoned."),
          p("You run the program on your own computer. Andre never receives your Schwab password, app secret, balance, positions, or private encryption key."),
          p("Trading can lose money. Options can lose their entire value quickly. The copier is a tool, not investment advice, account management, or a promise of results.", "Danger"),
          p("Three operational facts", "H2x"),
          bullets(["Your computer must remain awake and connected while you hold copied positions.",
                   "Schwab requires each person to reconnect about every seven days.",
                   "Use Approve first and practice mode until you understand every screen."]),
          p("Official resources", "H2x")]
resources = [[p("Installation page", "Smallx"), p("https://dre15w1.github.io/trading-copier-install/", "Smallx")],
             [p("Checksums", "Smallx"), p("https://github.com/dre15w1/trading-copier-install/releases/latest/download/SHA256SUMS.txt", "Smallx")]]
t = Table(resources, colWidths=[1.25 * inch, 5.15 * inch])
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PANEL), ("GRID", (0, 0), (-1, -1), .5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
story += [t, PageBreak()]

story += heading("The complete setup in one page", "Section 2")
story += [numbered([
    "Create your personal Schwab developer app and wait until Schwab marks it <b>Ready for Use</b>.",
    "Open the official installation page, read the disclosures, sign the agreement, and choose the download for your computer.",
    "Run the copier. It opens a local setup page at <b>http://127.0.0.1:8765</b>.",
    "The app creates its private connection locally and displays one <b>TV1- device code</b>.",
    "Click <b>Copy device code</b> and send the complete TV1- code to Andre. Never send your Schwab secret or private key.",
    "Andre opens Signal Access, pastes your code, and grants specific strategies.",
    "Wait for the app to show <b>Connected to Andre</b>, connect Schwab, choose limits, and leave <b>Approve first</b> selected.",
    "Receive a synthetic test entry and exit before considering live execution.",
    "Enable start at login and prevent the computer from sleeping during market hours.",
]),
          p("The TV1- code is safe to send. It contains a device identifier and public key only. The private key stays in Windows Credential Manager, macOS Keychain, or the app's protected local fallback. After Andre enables the device, a private non-trading connection check confirms that exact installation can receive messages.", "Callout"),
          PageBreak()]

story += heading("Create your Schwab developer app", "Section 3")
story += [p("Go to https://developer.schwab.com, create an Individual developer account, and create an app for your own brokerage account. Approval often takes several business days."),
          p("Use these values", "H2x")]
data = [[p("Field", "Smallx"), p("Value", "Smallx")],
        [p("API product", "Smallx"), p("Accounts and Trading Production; add Market Data Production if offered", "Smallx")],
        [p("App name", "Smallx"), p("Any simple personal name, such as Jane Copier", "Smallx")],
        [p("Callback URL", "Smallx"), p("https://127.0.0.1:8182/callback", "Smallx")],
        [p("Description", "Smallx"), p("Personal trading automation for my own self-directed account", "Smallx")]]
t = Table(data, colWidths=[1.45 * inch, 4.95 * inch], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), PANEL2), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("BACKGROUND", (0, 1), (-1, -1), PANEL), ("GRID", (0, 0), (-1, -1), .5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
story += [t, p("The callback must match exactly. A trailing slash, localhost in place of 127.0.0.1, or a different scheme can break authorization. Changing it after approval may send the app back through review.", "Danger"),
          p("When the app becomes Ready for Use, copy its App Key/Client ID and Secret/Client Secret into the copier setup screen. Do not send either value to Andre."), PageBreak()]

story += heading("Download the correct app", "Section 4")
story += [p("Use the official installation page. The three downloads are separate because Windows and the two Mac CPU families require different native executables."),
          p("Windows 10 or 11 - 64-bit", "H2x"),
          p("https://github.com/dre15w1/trading-copier-install/releases/latest/download/Trading-Copier-Setup.exe", "Codex"),
          p("Mac with Apple Silicon - M1, M2, M3, M4, or newer", "H2x"),
          p("https://github.com/dre15w1/trading-copier-install/releases/latest/download/copier-agent-macos-apple-silicon", "Codex"),
          p("Mac with an Intel processor", "H2x"),
          p("https://github.com/dre15w1/trading-copier-install/releases/latest/download/copier-agent-macos-intel", "Codex"),
          p("On a Mac, choose Apple menu > About This Mac. If it says Chip and begins with Apple M, choose Apple Silicon. If it says Processor and mentions Intel, choose Intel.", "Callout"),
          p("Only download from the official page. These builds are currently unsigned, so your operating system will warn you. A copy sent through email, text, AirDrop, or an unfamiliar link should not be run."), PageBreak()]

story += heading("Updating without setting up again", "Section 4A")
story += [p("Install the new version over the old one. Windows and Mac updates preserve the existing <b>.trading-copier</b> data folder, device identity, private key, Schwab app details, account selection, limits, and local history."),
          numbered(["Quit the running copier from its footer before replacing it.",
                    "Download the newest build for the same operating system and Mac architecture.",
                    "Install or launch the replacement normally.",
                    "Confirm the Home screen shows <b>Connected to Andre</b> and the expected Schwab account.",
                    "Only send Andre a new TV1- code if the app explicitly says the device must be relinked or this is a different computer."]),
          p("Do not select any option that creates a brand-new identity during a routine update. Existing users should not have to exchange keys again.", "Callout"), PageBreak()]

story += heading("Run it on Windows", "Section 5")
story += [numbered(["Open your Downloads folder.",
                    "Double-click <b>Trading-Copier-Setup.exe</b> and follow the installer.",
                    "If Windows SmartScreen appears, verify the filename, select <b>More info</b>, then <b>Run anyway</b>.",
                    "Your browser opens <b>http://127.0.0.1:8765</b>. That address means the page is served only by your own computer."]),
          p("Practice mode", "H2x"),
          p("Open PowerShell and run:", "Bodyx"),
          p('&amp; "$env:LOCALAPPDATA\\Programs\\Trading Copier\\Trading Copier.exe" --dry-run', "Codex"),
          p("Practice mode receives signals and exercises the workflow but sends no real order to Schwab. Confirm the practice banner is visible."), PageBreak()]

story += heading("Run it on a Mac", "Section 6")
story += [p("Download the correct Mac build first. Open Terminal, paste the full block below, and press Return. It selects the filename that matches your Mac CPU."),
          p('if [ "$(uname -m)" = "arm64" ]; then<br/>  FILE="$HOME/Downloads/copier-agent-macos-apple-silicon"<br/>else<br/>  FILE="$HOME/Downloads/copier-agent-macos-intel"<br/>fi<br/>chmod +x "$FILE"<br/>xattr -d com.apple.quarantine "$FILE"<br/>"$FILE"', "Codex"),
          p("For practice mode, use the same selection block but make the last line:", "Bodyx"),
          p('"$FILE" --dry-run', "Codex"),
          p("If Terminal says No such file or directory, confirm the file is in Downloads and that its name has no (1) suffix. If it says Bad CPU type in executable, you downloaded the wrong Mac architecture; delete it and choose the other Mac button.", "Callout"), PageBreak()]

story += heading("Setup wizard - device and Schwab", "Section 7")
story += [p("Step 1 - Connect to Andre", "H2x"),
          numbered(["The app creates its private connection automatically.",
                    "Click <b>Copy code</b>. The complete value begins with <b>TV1-</b>.",
                    "Send the complete TV1- code to Andre. No signal key is entered or sent.",
                    "Keep the app open. Andre's app sends a signed, non-trading confirmation to this device; the page then displays <b>Connected to Andre</b> and advances automatically."]),
          p("Do not send screenshots of Schwab credentials. Do not send files from the .trading-copier folder. Andre needs only the TV1- device code for signal access.", "Danger"),
          p("If you replace your computer, the new installation gets a new code. Send the new TV1- code to Andre so he can replace the old device. The old computer then stops receiving future entries."), PageBreak()]

story += heading("Setup wizard - account and limits", "Section 8")
story += [p("Signal connection", "H2x"),
          bullets(["The signal source and Andre's verification key are built into the app.",
                   "Subscribers never enter a repository address or publisher key.",
                   "The app rejects signals that do not match the built-in verification key."]),
          p("Step 2 - Connect Schwab", "H2x"),
          bullets(["Paste your App Key and Secret from your approved Schwab developer app.",
                   "Keep the callback URL identical to the registered value.",
                   "Click Connect Schwab, sign in on Schwab's website, and approve.",
                   "If the browser does not return automatically, copy the entire callback address and use the setup page's paste box."]),
          p("Step 3 - Choose the account", "H2x"),
          bullets(["Choose the intended Schwab account. Other accounts are left alone."]),
          p("Step 4 - Choose limits", "H2x"),
          bullets(["Start with a small risk percentage and low maximum position count.",
                   "Leave Approve first selected. Automatic execution requires a separate acknowledgement.",
                   "Keep publisher exits enabled so an accepted trade can be closed when Andre closes it."]),
          p("Step 5 - Finish", "H2x"),
          bullets(["Confirm Schwab is connected to the intended account.",
                   "Enable start at login and keep the computer awake."]), PageBreak()]

story += heading("What Andre does in Signal Access", "Section 9")
story += [p("On Andre's computer, Signal Access runs locally at http://127.0.0.1:8788. It is not a public website."),
          numbered(["Click <b>Add someone</b>.",
                    "Paste the friend's complete TV1- device code.",
                    "Select the strategies that person may receive.",
                    "Record the signed agreement if required, then save.",
                    "Signal Access sends a private connection check addressed only to that device. The subscriber sees confirmation without placing a trade.",
                    "Send a synthetic entry and exit before any live use."]),
          p("Revocation", "H2x"),
          p("Removing a strategy or disabling a subscriber stops new entries from being encrypted to that device. A subscriber who already entered a position continues receiving the corresponding exit, preventing revocation from stranding an open trade."),
          p("The private key never reaches Andre. Signal Access imports only the public device code and cannot generate the friend's private half.", "Callout"), PageBreak()]

story += heading("Test before live trading", "Section 10")
story += [numbered(["Keep the subscriber app in practice mode and Approve first mode.",
                    "Andre publishes a synthetic test entry for one granted strategy.",
                    "Confirm the test signal appears and is clearly labeled synthetic.",
                    "Approve it and confirm no real Schwab order is sent in practice mode.",
                    "Confirm the matching synthetic exit arrives.",
                    "Restart the app and confirm it opens normally and still shows the same TV1- device code in Settings."]),
          p("Do not switch to live execution if the test entry or exit is missing, Schwab shows the wrong account, or the app reports an uncertain order.", "Danger"),
          p("After practice", "H2x"),
          p("Watch the system for several sessions. When you intentionally leave practice mode, keep Approve first enabled and start with the smallest sensible risk."), PageBreak()]

story += heading("Using the copier day to day", "Section 11")
story += [bullets(["Leave the agent running and the computer awake whenever a copied position is open.",
                   "Review symbol, direction, contract, quantity, maximum cost, stop, and strategy before approving.",
                   "Decline anything you do not understand. Missing a trade is safer than approving blindly.",
                   "If an order is marked uncertain, check Schwab before trying anything again. Never assume it failed.",
                   "Use the copier's Positions page or Schwab directly to close a position when necessary.",
                   "Reconnect Schwab before the seven-day authorization expires."]),
          p("Weekly reconnect", "H2x"),
          numbered(["Choose a consistent evening each week, such as Sunday.",
                    "Click Reconnect Schwab in the copier.",
                    "Sign in on Schwab's website and approve.",
                    "If needed, paste the full callback URL into the copier's recovery box.",
                    "Confirm the dashboard shows roughly seven days remaining."]), PageBreak()]

story += heading("Long Term and shared-account partitions", "Section 12")
story += [p("The native Long Term screen is optional. It can research tickers, scan a watchlist, show holdings, prepare trim or exit proposals, find covered-call candidates, and submit an approved proposal through your own connected Schwab account."),
          p("Partition before buying", "H2x"),
          numbered(["Open <b>Long Term</b> from the navigation.",
                    "Set the percentage of account equity reserved for Long Term. It starts at <b>0%</b>, so it cannot open a position until you choose an amount.",
                    "The copied/short-term side sizes from the remaining percentage. For example, 25% Long Term leaves 75% for short-term sizing.",
                    "Review the committed amount on the screen before creating another opening proposal."]),
          p("Both sides also recheck live broker buying power. A partition is a software limit, not a separate Schwab subaccount; Schwab still reports one combined balance.", "Callout"),
          p("Approval is the default", "H2x"),
          bullets(["Research does not place an order.",
                   "Buy, add, trim, exit, and covered-call actions enter the approval queue.",
                   "Immediately before submission the app rechecks the partition, buying power, owned shares, covered shares, and live bid/ask spread.",
                   "An uncertain broker response is never retried automatically; inspect Schwab first.",
                   "Automatic Long Term execution is a separate override with its own acknowledgement. Ordinary copier automation does not enable it."]), PageBreak()]

story += heading("Optional AI - choose one of three providers", "Section 13")
story += [p("Long Term works in <b>No AI</b> mode. If you choose a provider, it is your provider account, key, usage, and bill. Andre's LLM credentials are not present in the subscriber app and cannot be borrowed as a fallback.", "Danger"),
          p("OpenAI", "H2x"),
          numbered(["Open https://platform.openai.com/docs/quickstart/make-your-first-api-request and create your own API account and API key.",
                    "Add API billing or credits. A ChatGPT subscription does not include API usage.",
                    "Review the current provider prices at https://openai.com/api/pricing/ and use the provider dashboard to set a spending limit if available.",
                    "In Long Term, choose OpenAI, enter a supported model name and paste the key, acknowledge direct billing, save, and click <b>Test connection</b>.",
                    "Run one ticker before a watchlist scan. Use <b>Delete saved key</b> to remove it from this computer."]),
          p("Anthropic", "H2x"),
          numbered(["Open https://console.anthropic.com/, create your own account, enable API billing, and create an API key.",
                    "Review current prices and model names at https://docs.anthropic.com/en/docs/about-claude/pricing.",
                    "In Long Term, choose Anthropic, enter a supported model name and paste the key, acknowledge direct billing, save, and test.",
                    "Run one ticker first. Delete the saved key from the screen when changing providers or retiring the computer."]),
          p("Provider prices and model availability change. The links above are authoritative. Deep scans can make one paid call per ticker; the app does not promise a fixed dollar cost.", "Callout"), PageBreak()]

story += heading("Optional local AI with Ollama", "Section 14")
story += [p("Ollama has no per-call provider bill, but model downloads can use tens of gigabytes and analysis uses memory, CPU or GPU time, electricity, and your hardware. Intel Macs use CPU-only execution and may be slow."),
          numbered(["Install Ollama from https://ollama.com/download. The current Ollama requirements may be newer than the copier's own operating-system requirements, so check that page first.",
                    "Open PowerShell on Windows or Terminal on Mac and run <b>ollama run llama3.2</b>. Wait for the model download and one successful response.",
                    "Keep Ollama running. In the copier's Long Term screen choose <b>Ollama (local)</b>.",
                    "Keep the local URL <b>http://127.0.0.1:11434</b>, enter <b>llama3.2</b> as the model, save, and test.",
                    "Run one-ticker research before scanning a watchlist."]),
          p("The copier accepts only a loopback Ollama address in this release. It will reject a remote hostname so portfolio facts are not silently sent to an unreviewed server.", "Callout"),
          p("If the test fails", "H2x"),
          bullets(["Start the Ollama application and try again.",
                   "If the model is missing, run ollama run llama3.2 and let it finish downloading.",
                   "If the computer runs out of memory or becomes too slow, choose No AI or a smaller local model.",
                   "OpenAI/Anthropic 401 or 403 errors usually mean the key or billing is not ready; 429 means a provider usage or rate limit. Check the provider dashboard."]), PageBreak()]

story += heading("Troubleshooting", "Section 15")
trouble = [[p("Problem", "Smallx"), p("What to do", "Smallx")],
           [p("Windows protected your PC", "Smallx"), p("Verify the official filename and source, then More info > Run anyway.", "Smallx")],
           [p("Mac says damaged or cannot verify", "Smallx"), p("Run chmod and xattr commands from section 6 against the correct architecture file.", "Smallx")],
           [p("Bad CPU type", "Smallx"), p("Delete the file and download the other Mac architecture.", "Smallx")],
           [p("No such file or directory", "Smallx"), p("Check Downloads and remove any (1) suffix by downloading once cleanly.", "Smallx")],
           [p("Still says Waiting for Andre", "Smallx"), p("Leave the app open for one minute. Andre should open Signal Access, verify the exact TV1- device, and press the private connection check. If this is an upgrade, do not create another identity.", "Smallx")],
           [p("No signals", "Smallx"), p("Check for a recent private connection check first. Only new live filled short-term trades are eligible; paper activity and Long Term activity are intentionally not published.", "Smallx")],
           [p("Mac time warning / SSL certificate", "Smallx"), p("The copier keeps retrying authoritative time sources. Update macOS and system certificates, verify Date & Time is automatic, then restart. Do not rely on a custom entry-hours window until the warning clears; exits are never blocked by the clock.", "Smallx")],
           [p("Fingerprint changed", "Smallx"), p("Stop. Confirm with Andre by phone before accepting any change.", "Smallx")],
           [p("Schwab connection expired", "Smallx"), p("Reconnect immediately. No entry or exit can be submitted until authorization is restored.", "Smallx")],
           [p("Uncertain order", "Smallx"), p("Open Schwab and inspect orders and positions. Do not resubmit automatically.", "Smallx")]]
t = Table(trouble, colWidths=[1.8 * inch, 4.6 * inch], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), PANEL2), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PANEL, PANEL2]), ("GRID", (0, 0), (-1, -1), .5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
story += [t, p("If you are confused while holding a real position, the safe move is to check Schwab, close the position if appropriate, and call Andre. Your Schwab account remains the final source of truth.", "Danger"), PageBreak()]

story += heading("Security and storage", "Appendix")
story += [p("Local folder", "H2x"),
          p("Windows: C:\\Users\\&lt;you&gt;\\.trading-copier\\<br/>macOS: ~/.trading-copier/", "Codex"),
          bullets(["agent.json contains settings and is designed not to contain secrets.",
                   "state.db contains local positions, approvals, and history.",
                   "agent.log records operational events for troubleshooting.",
                   "Secrets are stored in Windows Credential Manager or macOS Keychain when available."]),
          p("Never share", "H2x"),
          bullets(["Schwab username, password, App Secret, or refresh authorization.",
                   "The copier private encryption key or secrets.json fallback.",
                   "Remote-control access to the computer while Schwab is open."]),
          p("Safe to share with Andre", "H2x"),
          bullets(["The complete TV1- device code shown by the copier.",
                   "A redacted screenshot of a non-secret error page or the app log when requested."]),
          Spacer(1, .25 * inch),
          p("Trading Copier - Setup and Use Guide. Revised 14 August 2026 for agent version 0.13.7. The software and this document are provided as-is, without warranty. Nothing here is investment advice. Trading involves risk of loss.", "Smallx"),
          p("Copyright 2026 Walkers Software LLC. All rights reserved.", "Smallx")]


GuideDoc(str(OUT)).build(story)
print(OUT)
