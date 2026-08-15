"""Build the detailed Trading Copier installation guide and user manual."""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "manual-assets"
OUT = ROOT / "Trading-Copier-Setup-Guide.pdf"
VERSION = "0.13.10"

BG = colors.HexColor("#0d1117")
PANEL = colors.HexColor("#161b22")
PANEL2 = colors.HexColor("#1c2128")
LINE = colors.HexColor("#30363d")
INK = colors.HexColor("#e6edf3")
MUTED = colors.HexColor("#9aa5b1")
BLUE = colors.HexColor("#58a6ff")
GREEN = colors.HexColor("#3fb950")
AMBER = colors.HexColor("#d29922")
RED = colors.HexColor("#ff7b72")


class ManualDoc(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            pagesize=letter,
            rightMargin=48,
            leftMargin=48,
            topMargin=55,
            bottomMargin=52,
            title=f"Trading Copier Installation Guide and User Manual v{VERSION} / schema v2",
            author="Walkers Software LLC",
            subject="Beginner installation, operation, schema v2 multi-leg options, trading concepts, and strategy manual",
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates(PageTemplate(id="manual", frames=[frame], onPage=self._decorate))

    def _decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BG)
        canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        canvas.setStrokeColor(LINE)
        canvas.line(48, 39, letter[0] - 48, 39)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(48, 26, f"TEAM VILLAIN  /  Trading Copier v{VERSION}")
        canvas.drawRightString(letter[0] - 48, 26, f"Page {doc.page}")
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            if style in ("Chapter", "Section"):
                level = 0 if style == "Chapter" else 1
                text = flowable.getPlainText()
                key = f"h{level}-{self.page}-{abs(hash(text))}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level, closed=False)
                self.notify("TOCEntry", (level, text, self.page, key))


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
                          fontSize=27, leading=32, textColor=colors.white, alignment=TA_CENTER,
                          spaceAfter=10))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=12.5,
                          leading=18, textColor=colors.HexColor("#d8e3ef"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="Chapter", parent=styles["Heading1"], fontName="Helvetica-Bold",
                          fontSize=22, leading=26, textColor=INK, spaceAfter=12,
                          keepWithNext=True))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold",
                          fontSize=15, leading=19, textColor=BLUE, spaceBefore=12,
                          spaceAfter=7, keepWithNext=True))
styles.add(ParagraphStyle(name="Subsection", parent=styles["Heading3"], fontName="Helvetica-Bold",
                          fontSize=11.5, leading=15, textColor=INK, spaceBefore=8,
                          spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontName="Helvetica",
                          fontSize=9.4, leading=13.5, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8,
                          leading=11, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="Kicker", parent=styles["BodyText"], fontName="Helvetica-Bold",
                          fontSize=7.6, leading=10, textColor=MUTED, spaceAfter=5,
                          spaceBefore=2))
styles.add(ParagraphStyle(name="CodeX", parent=styles["Code"], fontName="Courier",
                          fontSize=7.6, leading=10.5, textColor=INK, backColor=PANEL2,
                          borderColor=LINE, borderWidth=.7, borderPadding=7,
                          spaceBefore=4, spaceAfter=8))
styles.add(ParagraphStyle(name="Note", parent=styles["BodyText"], fontSize=9.2,
                          leading=13.2, textColor=INK, backColor=PANEL2, borderColor=BLUE,
                          borderWidth=1, borderPadding=9, spaceBefore=5, spaceAfter=8))
styles.add(ParagraphStyle(name="Good", parent=styles["Note"], textColor=GREEN,
                          borderColor=GREEN, backColor=colors.HexColor("#0f2417")))
styles.add(ParagraphStyle(name="Warn", parent=styles["Note"], textColor=AMBER,
                          borderColor=AMBER, backColor=colors.HexColor("#271d09")))
styles.add(ParagraphStyle(name="Danger", parent=styles["Note"], textColor=RED,
                          borderColor=RED, backColor=colors.HexColor("#2a1315")))
styles.add(ParagraphStyle(name="Caption", parent=styles["Small"], fontSize=7.8,
                          leading=10.5, alignment=TA_CENTER, textColor=MUTED,
                          spaceBefore=4, spaceAfter=8))


def p(text: str, style: str = "Body") -> Paragraph:
    return Paragraph(text, styles[style])


def bullets(items, numbered: bool = False):
    return ListFlowable(
        [ListItem(p(item), leftIndent=12) for item in items],
        bulletType="1" if numbered else "bullet",
        start="1",
        leftIndent=23,
        bulletFontName="Helvetica-Bold",
        bulletFontSize=8,
        bulletColor=BLUE,
        spaceAfter=7,
    )


def chapter(title: str, kicker: str | None = None):
    output = []
    if kicker:
        output.append(p(kicker.upper(), "Kicker"))
    output.append(p(title, "Chapter"))
    return output


def section(title: str):
    return p(title, "Section")


def screen(filename: str, caption: str, max_height: float = 5.15 * inch):
    path = ASSETS / filename
    image = Image(str(path))
    max_width = 6.65 * inch
    ratio = min(max_width / image.imageWidth, max_height / image.imageHeight)
    image.drawWidth = image.imageWidth * ratio
    image.drawHeight = image.imageHeight * ratio
    image.hAlign = "CENTER"
    return [image, p(caption, "Caption")]


def screenshot_page(title: str, filename: str, caption: str, steps: list[str]):
    return chapter(title, "SCREEN WALKTHROUGH") + screen(filename, caption, 4.55 * inch) + [
        section("What to look for"), bullets(steps, numbered=True), PageBreak()
    ]


def two_col(rows, widths=(1.6 * inch, 4.9 * inch), header=True):
    table = Table([[p(cell, "Small") for cell in row] for row in rows], colWidths=list(widths),
                  repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), .5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [PANEL, PANEL2]),
    ]
    if header:
        commands.extend([("BACKGROUND", (0, 0), (-1, 0), PANEL2),
                         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)])
    table.setStyle(TableStyle(commands))
    return table


class ConnectionDiagram(Flowable):
    def __init__(self):
        super().__init__()
        self.width = 6.65 * inch
        self.height = 2.05 * inch

    def draw(self):
        c = self.canv
        boxes = [
            (0, "Andre's\nLIVE filled trade"),
            (1.72 * inch, "Encrypted copy\nfor this device"),
            (3.44 * inch, "Subscriber copier\nchecks signature"),
            (5.16 * inch, "Approve / execute\nin own Schwab"),
        ]
        for x, label in boxes:
            c.setFillColor(PANEL2)
            c.setStrokeColor(BLUE)
            c.roundRect(x, .65 * inch, 1.45 * inch, .82 * inch, 8, fill=1, stroke=1)
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 8.5)
            for line_no, line in enumerate(label.split("\n")):
                c.drawCentredString(x + .725 * inch, 1.15 * inch - line_no * 12, line)
        c.setStrokeColor(GREEN)
        c.setLineWidth(2)
        for x in (1.48 * inch, 3.20 * inch, 4.92 * inch):
            c.line(x, 1.05 * inch, x + .20 * inch, 1.05 * inch)
            c.line(x + .14 * inch, 1.10 * inch, x + .20 * inch, 1.05 * inch)
            c.line(x + .14 * inch, 1.00 * inch, x + .20 * inch, 1.05 * inch)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.5)
        c.drawString(0, .34 * inch, "Paper trades and Long Term actions do not enter this signal path.")
        c.drawString(0, .14 * inch, "The private key and Schwab credentials never leave the subscriber's computer.")


class CredentialDiagram(Flowable):
    """Show which credential is created where and where it may travel."""

    def __init__(self):
        super().__init__()
        self.width = 6.65 * inch
        self.height = 3.15 * inch

    def draw(self):
        c = self.canv
        rows = [
            ("Schwab username + password", "Already owned by subscriber", "Typed only on Schwab's website", RED),
            ("App Key / Client ID", "Created in Schwab Developer Portal", "Pasted into this subscriber's copier", BLUE),
            ("Secret / Client Secret", "Created in Schwab Developer Portal", "Pasted once; never sent to Andre", AMBER),
            ("TV1- connection code", "Created by the copier", "The only code sent to Andre", GREEN),
        ]
        widths = (2.05 * inch, 2.15 * inch, 2.25 * inch)
        y = 2.72 * inch
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(MUTED)
        for x, label in zip((0, widths[0], widths[0] + widths[1]),
                            ("ITEM", "WHERE IT COMES FROM", "WHERE IT GOES")):
            c.drawString(x + 8, y + 10, label)
        for name, origin, destination, accent in rows:
            y -= .60 * inch
            x = 0
            for width, text_value in zip(widths, (name, origin, destination)):
                c.setFillColor(PANEL2)
                c.setStrokeColor(LINE)
                c.roundRect(x, y, width - 5, .48 * inch, 5, fill=1, stroke=1)
                c.setFillColor(accent if x == 0 else INK)
                font_name = "Helvetica-Bold" if x == 0 else "Helvetica"
                c.setFont(font_name, 7.8)
                words = text_value.split()
                lines, current = [], ""
                for word in words:
                    candidate = (current + " " + word).strip()
                    if c.stringWidth(candidate, font_name, 7.8) > width - 20 and current:
                        lines.append(current); current = word
                    else:
                        current = candidate
                if current:
                    lines.append(current)
                for n, line in enumerate(lines[:2]):
                    c.drawString(x + 8, y + 21 - n * 10, line)
                x += width


story = []

# Cover
hero = Image(str(ROOT / "tv-hero.jpg"), width=7.0 * inch, height=3.94 * inch)
hero.hAlign = "CENTER"
cover = Table([[[hero, Spacer(1, .28 * inch), p("Trading Copier", "CoverTitle"),
                 p("Installation Guide + Complete User Manual", "CoverTitle"),
                 Spacer(1, .05 * inch),
                 p(f"Version {VERSION} / Windows and macOS", "CoverSub"),
                 p("Written for first-time investors and first-time copier users", "CoverSub"),
                 p("Revised 15 August 2026 / schema v2 multi-leg paper support", "CoverSub")]]],
              colWidths=[letter[0] - 96], rowHeights=[6.9 * inch])
cover.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BG),
                           ("BOX", (0, 0), (-1, -1), 1, LINE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0)]))
story += [cover, PageBreak()]

story += chapter("How to use this manual", "START HERE")
story += [p("This book has two jobs. Part One gets the copier installed and connected. Part Two teaches you how to operate it safely every day. The later chapters explain the trading language and every signal type so a new investor can understand what the screen means before approving anything."),
          p("A screenshot shows the real program. A chart is an educational drawing of a setup, not a promise that price will follow the drawing.", "Note"),
          section("The safest learning order"),
          bullets(["Read Trading basics before approving an options trade.",
                   "Install and complete the five setup steps.",
                   "Stay in Approve first mode and use the smallest practical risk.",
                   "Confirm the private connection check and Schwab account before market hours.",
                   "Learn the Signal Types page. Turn off anything you do not understand.",
                   "Use practice mode and a synthetic entry/exit before live execution."], numbered=True),
          p("Nothing in this manual is investment advice or a guarantee. A technically correct copier can still execute a losing trade. Options can lose 100% of their value.", "Danger"), PageBreak()]

story += [p("Contents", "Chapter")]
toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle(name="TOC0", fontName="Helvetica-Bold", fontSize=10.5,
                   leading=15, leftIndent=0, firstLineIndent=0, textColor=INK, spaceBefore=5),
    ParagraphStyle(name="TOC1", fontName="Helvetica", fontSize=8.5,
                   leading=12, leftIndent=16, firstLineIndent=0, textColor=MUTED),
]
story += [toc, PageBreak()]

story += chapter("What the copier does - and does not do", "PART 1 / ORIENTATION")
story += [p("The Trading Copier watches a private signal feed, verifies that a message really came from Andre, checks that the exact device is allowed to receive that strategy, applies the subscriber's own limits, and then either asks for approval or submits the order when automatic execution has been separately enabled."),
          ConnectionDiagram(), Spacer(1, 8),
          section("Eligible messages"),
          bullets(["Only a new <b>live, filled, short-term</b> trade is published as an entry signal.",
                   "Paper activity is ignored.",
                   "Long Term activity is independent and is not copied.",
                   "A private connection check can confirm one device without creating an order.",
                   "Exits continue for an already accepted copied position even if that strategy is later turned off."]),
          section("What stays private"),
          bullets(["Schwab username and password", "Schwab developer app secret",
                   "The copier's private encryption key", "Account balances and positions",
                   "The subscriber's local limits and muted signal types"]), PageBreak()]

story += chapter("Trading basics for a first-time investor", "PART 2 / LEARN BEFORE YOU APPROVE")
story += [section("Stocks, shares, and options"),
          two_col([
              ["Term", "Plain-language meaning"],
              ["Stock / share", "A small ownership unit in a company or fund. One share rises or falls dollar-for-dollar with its quoted price."],
              ["Call option", "A time-limited contract that generally gains value when the underlying rises. Buying a call does not guarantee a profit even when the stock rises."],
              ["Put option", "A time-limited contract that generally gains value when the underlying falls."],
              ["Contract", "One standard equity-option contract usually represents 100 shares. A quoted premium of $1.25 normally costs about $125 before fees."],
              ["Expiration", "The last date the option exists. A 0DTE option expires the same trading day and can lose value extremely quickly."],
          ]),
          section("The five prices you must recognize"),
          bullets(["<b>Bid:</b> the highest displayed price a buyer currently offers.",
                   "<b>Ask:</b> the lowest displayed price a seller currently offers.",
                   "<b>Spread:</b> ask minus bid. A wide spread increases slippage and makes exits harder.",
                   "<b>Entry:</b> the price at which the trade is opened.",
                   "<b>Stop and target:</b> the planned loss exit and profit exit. Neither guarantees that an order fills at exactly that price."]),
          p("Example: an option quoted $1.20 bid / $1.30 ask has a $0.10 spread. Buying one contract near $1.30 is about $130. If it falls to $0.65, the position has lost about $65, or 50%, before fees.", "Warn"),
          section("Risk, R, and position size"),
          p("Many strategy explanations use <b>R</b>. R is the planned distance from entry to stop. If the entry is $100 and the stop is $98, then 1R is $2 per share. A 2R target is $104. The copier's risk percentage and buying-power checks still decide the actual order size."),
          p("Never assume a stop limits the loss perfectly. A gap, halt, fast option market, rejected order, expired authorization, or lost connection can produce a worse result.", "Danger"), PageBreak()]

story += chapter("Orders, fills, exits, and uncertainty", "TRADING BASICS")
story += [section("An alert is not the same thing as a fill"),
          bullets(["A <b>signal</b> is the publisher's instruction.",
                   "An <b>approval</b> is your permission for the copier to continue.",
                   "An <b>order</b> is the request sent to Schwab.",
                   "A <b>fill</b> means Schwab reports that some or all of the order executed.",
                   "A <b>position</b> is what the broker says you now own."], numbered=True),
          section("Why uncertain means stop and inspect"),
          p("A network interruption can happen after Schwab receives an order but before the copier receives the reply. Retrying blindly could double the position. When the copier says an order is uncertain, open Schwab and inspect Orders and Positions before taking another action.", "Danger"),
          section("Short-term versus long-term"),
          two_col([
              ["Short Term", "Long Term"],
              ["Starts from eligible live signals", "Independent of signals"],
              ["Usually minutes, hours, or a few days", "Portfolio work measured in weeks, months, or longer"],
              ["Shown on Short Term and Approvals", "Shown in the separate Long Term area"],
              ["Publisher exits can close an accepted copied position", "You create and approve your own buy, add, trim, exit, or covered-call proposal"],
          ]), PageBreak()]

story += chapter("Install on Windows", "PART 3 / INSTALLATION")
story += [section("Before downloading"),
          bullets(["Use Windows 10 or 11, 64-bit.", "Install pending Windows updates.",
                   "Make sure the computer's Date & Time is automatic.",
                   "Use a Windows account you control and can sign into."], numbered=True),
          section("Download and install"),
          bullets(["Open https://dre15w1.github.io/trading-copier-install/.",
                   "Read the disclosures and agreement, then choose <b>Download for Windows</b>.",
                   "Open Downloads and double-click <b>Trading-Copier-Setup.exe</b>.",
                   "If SmartScreen appears, confirm the filename and official source, choose <b>More info</b>, then <b>Run anyway</b>.",
                   "Complete the installer. Use the Trading Copier shortcut in the Start menu or on the desktop.",
                   "The browser opens the local address shown by the app. 127.0.0.1 means this computer, not a public website."], numbered=True),
          p("Do not download a copy sent through email, text, or an unfamiliar file-sharing link. Use the official page every time.", "Danger"),
          section("Practice mode"),
          p('&amp; "$env:LOCALAPPDATA\\Programs\\Trading Copier\\Trading Copier.exe" --dry-run', "CodeX"),
          p("Practice mode exercises the workflow but does not submit real orders. Confirm the practice banner is visible."), PageBreak()]

story += chapter("Install on a Mac", "PART 3 / INSTALLATION")
story += [section("Choose the correct Mac"),
          bullets(["Apple menu > About This Mac.",
                   "If Chip begins with Apple M, download Apple Silicon.",
                   "If Processor mentions Intel, download Intel."], numbered=True),
          section("Download and run"),
          p('if [ "$(uname -m)" = "arm64" ]; then<br/>  FILE="$HOME/Downloads/copier-agent-macos-apple-silicon"<br/>else<br/>  FILE="$HOME/Downloads/copier-agent-macos-intel"<br/>fi<br/>chmod +x "$FILE"<br/>xattr -d com.apple.quarantine "$FILE"<br/>"$FILE"', "CodeX"),
          bullets(["Download exactly once so the filename does not gain a (1) suffix.",
                   "Open Terminal from Applications > Utilities.",
                   "Paste the full block and press Return.",
                   "Leave the copier running. Closing only the browser tab does not quit it.",
                   "Use the Quit Copier link in the footer when you intend to stop the program."], numbered=True),
          p("A certificate warning from the copier's time check is not a trading signal. Update macOS, verify automatic Date & Time, and restart. Do not rely on a custom entry-hours window until the warning clears. Exits are never blocked by the clock.", "Warn"), PageBreak()]

story += chapter("Create the required Schwab developer app", "PART 4 / FIRST SETUP")
story += [p("Every subscriber uses their own Schwab developer application. Andre's Schwab key is never entered into the subscriber copier. The developer application is what allows the copier on this computer to ask Schwab for permission to place orders in the account the subscriber chooses."),
          p("The developer account and the ordinary brokerage account are related but separate logins. Creating a developer account does not move money, open a trade, or give Andre access.", "Note"),
          CredentialDiagram(),
          p("The Secret is treated like a password. The TV1- code is the only one of these four items designed to be sent to Andre.", "Danger"),
          section("Before starting"),
          bullets(["Have access to the email address used for Schwab developer registration.",
                   "Know the subscriber's normal Schwab brokerage login, but do not send it to Andre.",
                   "Use the same computer that will run the copier when entering the App Key and Secret.",
                   "Write down the exact callback URL from this manual before creating the app."], numbered=True),
          PageBreak()]

story += chapter("Schwab portal - create the developer account", "SCHWAB APP KEY / STEP 1")
story += [p("Official starting address: <b>https://developer.schwab.com/</b>. Type or bookmark this address directly. Do not follow an API-key link sent by an unknown person."),
          bullets(["Open the official Schwab Developer Portal.",
                   "Choose the registration or sign-up option for an <b>Individual</b> developer account.",
                   "Enter the requested contact information and email address.",
                   "Open Schwab's verification email and complete the verification link.",
                   "Return to the Developer Portal and sign in.",
                   "If Schwab presents terms or an API agreement, read and accept them only for the subscriber's own account."], numbered=True),
          p("The portal's button names can change slightly. Look for the path that ends at the signed-in developer dashboard and a page named <b>My Apps</b>, <b>Apps</b>, or similar. Do not use the regular schwab.com brokerage page to look for an App Key; it is created in the Developer Portal.", "Note"),
          section("If registration does not finish"),
          bullets(["Check spam or junk mail for the verification message.",
                   "Make sure the verification link is opened in the same browser session.",
                   "Turn off aggressive popup blocking for developer.schwab.com only.",
                   "If the portal says the email already exists, use its password-recovery flow instead of creating duplicates."], numbered=True),
          PageBreak()]

story += chapter("Schwab portal - create the Trader API app", "SCHWAB APP KEY / STEP 2")
story += [p("After signing in, open <b>My Apps</b> and choose <b>Create App</b>, <b>Add App</b>, or the equivalent new-application button."),
          two_col([
              ["Field", "What to enter"],
              ["Application type", "Individual / personal use, when the portal asks"],
              ["Product", "Trader API / Accounts and Trading Production; add Market Data Production only if the portal offers or requires it"],
              ["App name", "A simple personal name such as Jane Trading Copier"],
              ["Callback URL", "https://127.0.0.1:8182/callback, character for character"],
              ["Description", "Personal trading automation for my own self-directed account"],
          ]),
          bullets(["Select the Trader API or Accounts and Trading product used for an individual brokerage account.",
                   "Enter a personal app name. It does not need to match the copier device name.",
                   "Paste the callback URL exactly as shown in the table.",
                   "Enter the personal-use description.",
                   "Review every field, then submit the app for Schwab's review."], numbered=True),
          p("A trailing slash, localhost instead of 127.0.0.1, http instead of https, a different port, or a spelling change can break authorization. Use exactly <b>https://127.0.0.1:8182/callback</b> unless the copier itself displays a different callback during setup.", "Danger"),
          PageBreak()]

story += chapter("Wait for approval, then find the App Key and Secret", "SCHWAB APP KEY / STEP 3")
story += [p("Submitting the app does not mean it is ready immediately. Return to My Apps and watch the status. Schwab may use wording such as Pending, In Review, Approved, or Ready for Use."),
          bullets(["Do not repeatedly delete and recreate a pending app; that can restart the process.",
                   "Wait until Schwab marks the app <b>Ready for Use</b> or otherwise approved for production.",
                   "Open the approved app's detail page.",
                   "Locate the value labeled <b>App Key</b>, <b>Client ID</b>, or equivalent. These names refer to the public identifier the copier calls App Key.",
                   "Locate the value labeled <b>Secret</b>, <b>Client Secret</b>, or equivalent.",
                   "Use the portal's reveal or copy control if the Secret is hidden. Copy it carefully without spaces before or after it."], numbered=True),
          p("Some portals show a Secret only once or require a regenerate action later. Save it directly into the copier rather than an email, text message, shared note, or screenshot.", "Warn"),
          section("How to tell the two values apart"),
          two_col([
              ["App Key / Client ID", "Identifies which developer app is requesting access. Enter it in the copier's App Key box."],
              ["Secret / Client Secret", "Proves the app is allowed to make that request. Enter it in the copier's Secret box. Never send it to Andre."],
          ], header=False),
          p("Neither value is the subscriber's Schwab password. Neither value is the TV1- connection code.", "Danger"), PageBreak()]

story += chapter("Put the Schwab credentials into the copier", "SCHWAB APP KEY / STEP 4")
story += [bullets(["Open the Trading Copier and continue to setup step 2, <b>Connect Schwab</b>.",
                   "In <b>App Key</b>, paste the portal's App Key or Client ID.",
                   "In <b>Secret</b>, paste the portal's Secret or Client Secret.",
                   "In <b>Callback URL</b>, confirm the address matches the approved developer app character for character.",
                   "Press <b>Save app details</b>.",
                   "The Secret moves into this computer's password vault. The copier does not display it again."], numbered=True),
          p("Do not paste the short fingerprint, TV1- code, Schwab password, or Andre's key into either Schwab credential field.", "Danger"),
          section("Now authorize the brokerage account"),
          bullets(["Press <b>Connect Schwab</b>.",
                   "A browser opens Schwab's own sign-in page.",
                   "Enter the subscriber's normal Schwab username and password on Schwab's page, not inside the copier.",
                   "Review the authorization request and approve it.",
                   "Return to the copier. It should show <b>Schwab is connected</b> and allow the subscriber to continue to account selection.",
                   "If the browser does not return, copy the entire address from the browser after authorization and paste it into the copier's recovery box."], numbered=True),
          p("A green <b>Schwab is connected</b> message is the authoritative status. The Connect Schwab button may remain available because it is also the way to reconnect later; its presence does not mean the connection failed.", "Good"),
          PageBreak()]

story += chapter("Schwab key problems and safe fixes", "SCHWAB APP KEY / TROUBLESHOOTING")
story += [two_col([
              ["Problem", "What to check"],
              ["Connect button disabled", "Save both App Key and Secret first."],
              ["Invalid client / unauthorized_client", "Confirm the App Key belongs to the approved app and was copied without spaces."],
              ["Invalid secret", "Return to the approved app, copy the Client Secret again, or use Schwab's regenerate process and replace the saved Secret."],
              ["Redirect or callback mismatch", "Compare scheme, 127.0.0.1, port 8182, /callback, capitalization, and trailing slash character for character."],
              ["App still pending", "The key cannot be used for production until Schwab approves it. Wait rather than recreating it."],
              ["Browser warning on callback", "The callback is this computer. Follow the copier's recovery instructions and paste the entire callback URL if automatic return fails."],
              ["Connected, but expires soon", "Reconnect through the copier. Schwab normally requires periodic reauthorization."],
              ["Changed or regenerated Secret", "Save the new Secret in the copier, then reconnect Schwab. Do not change the TV1- device identity."],
          ]),
          p("Support may ask for a screenshot of the portal status or callback setting. Black out the App Key, Secret, account numbers, authorization code, and personal information first. Never send the Secret even to Andre.", "Danger"),
          PageBreak()]

story += chapter("The five setup screens", "PART 4 / FIRST SETUP")
story += [section("1. Connect to Andre"),
          bullets(["The copier creates a private/public key pair on this computer.",
                   "Press Copy code and send the complete TV1- connection code to Andre.",
                   "The TV1- code contains the device ID and public key only. The private key stays on this computer.",
                   "Andre links the exact device and sends a private non-trading connection check.",
                   "When the screen says Connected to Andre, it advances automatically."], numbered=True),
          section("2. Connect Schwab"),
          bullets(["Save your own App Key, Secret, and exact callback URL.",
                   "Press Connect Schwab. Sign in only on Schwab's website.",
                   "Approve access and return to the copier.",
                   "If the browser cannot return, paste the entire callback address into the recovery field."], numbered=True),
          section("3. Choose account"),
          p("Select the intended masked account. Other Schwab accounts are left alone."),
          section("4. Your limits"),
          p("Begin with a small risk percentage, a low maximum number of open positions, a daily loss limit, and Approve first."),
          section("5. Finish"),
          p("Verify Signal connection, masked Schwab account, risk limits, approval mode, and password-vault status before pressing Start watching for signals.", "Good"), PageBreak()]

story += chapter("Update without exchanging keys again", "PART 4 / FIRST SETUP")
story += [p("A normal update installs over the old app and preserves the .trading-copier data folder, device identity, private key, Schwab app details, selected account, limits, and history on both Windows and Mac."),
          bullets(["Quit the running copier from its footer.",
                   "Download the latest build for the same operating system and Mac architecture.",
                   "Install or launch the replacement normally.",
                   "Confirm Home shows Connected to Andre and the expected masked Schwab account.",
                   "Send a new TV1- code only for a new computer or when the app explicitly requires relinking."], numbered=True),
          p("Do not choose Create a brand new key during a routine update. That deliberately creates a new identity and requires Andre to link it.", "Warn"), PageBreak()]

story += screenshot_page("Home screen", "screen-home.jpg",
                         "Home is the daily health check: signal connection, Schwab authorization, today's activity, and immediate controls.",
                         ["Signals from Andre should say Connected and show a recent check.",
                          "Schwab should say Connected and show the intended masked account.",
                          "Watch the reconnect countdown; Schwab authorization lasts about seven days.",
                          "Review open count, realized result, and approval mode.",
                          "Done for the day blocks new entries; it does not abandon exits."])

story += screenshot_page("Approvals screen", "screen-approvals.jpg",
                         "Approvals is where a new entry waits when Approve first is enabled.",
                         ["Read symbol, call/put direction, strategy, instrument, quantity, and maximum cost.",
                          "Compare the planned stop and target with the amount you can afford to lose.",
                          "Approve only when you understand the trade; otherwise decline.",
                          "After approval, wait for the broker result. Do not click repeatedly.",
                          "If status becomes uncertain, inspect Schwab before doing anything else."])

story += screenshot_page("Short Term screen", "screen-short-term.jpg",
                         "Short Term contains copied positions and the current trade state from eligible signals.",
                         ["Open positions came from accepted live short-term signals or a subscriber action on this side.",
                          "Use Trim to reduce size and Close to exit your own position.",
                          "A manual close affects your account; it does not close anyone else's trade.",
                          "Check Schwab after every manual action, especially if the response is delayed."])

story += screenshot_page("Signal Types screen", "screen-signal-types-1.jpg",
                         "Signal Types explains each strategy and lets the subscriber stop future entries from a strategy.",
                         ["Taking these means future eligible entries are allowed through your local filter.",
                          "Turn off stops new entries of that kind on this computer.",
                          "Turning off never blocks the exit for a copied position already open.",
                          "Open How this works before deciding whether to take a strategy."])

# Strategy catalogue
catalogue = json.loads((ASSETS / "strategy-catalogue.json").read_text(encoding="utf-8"))
for index, strategy in enumerate(catalogue, start=1):
    story += chapter(strategy["label"], f"PART 5 / STRATEGY {index} OF {len(catalogue)}")
    chips = [["Usual horizon", strategy.get("horizon", "unknown")],
             ["Usual instrument", strategy.get("instrument", "unknown")],
             ["Typical session", strategy.get("session", "See signal")]]
    story += [two_col([["Quick fact", "What the app says"]] + chips),
              section("The idea in one sentence"), p(strategy["one_liner"])]
    chart_path = ASSETS / "strategies" / f"{strategy['id']}.png"
    if chart_path.exists():
        chart = Image(str(chart_path), width=6.55 * inch, height=3.33 * inch)
        chart.hAlign = "CENTER"
        story += [chart, p("Educational setup drawing. The dashed levels show entry, stop, and take-profit logic; actual prices and fills vary.", "Caption")]
    if strategy.get("trigger"):
        story += [p(f"<b>What must happen before entry:</b> {strategy['trigger']}", "Note")]
    for part in strategy.get("how_it_works", []):
        story += [p(part["h"], "Subsection"), p(part["p"])]
    story += [p("Beginner decision: if you cannot explain the setup, stop, and exit in your own words, turn this signal type off until you can.", "Warn"), PageBreak()]

story += screenshot_page("Long Term overview", "screen-long-term-overview.jpg",
                         "Long Term is a separate portfolio workspace. It does not listen for or copy Andre's signals.",
                         ["Set a capital partition before creating a long-term opening proposal.",
                          "A 25% Long Term allocation leaves 75% for copied/short-term sizing.",
                          "The partition is a software limit inside one Schwab account, not a new broker subaccount.",
                          "Approval is required by default."])

story += screenshot_page("Long Term tools and research", "screen-long-term-tools.jpg",
                         "Long Term can research, scan, and prepare proposals; research alone does not place an order.",
                         ["Use ticker research or a watchlist scan to collect information.",
                          "Sector Rotation ranks areas of the market; it does not guarantee leadership will continue.",
                          "Review every proposal's side, quantity, estimated price, and reason.",
                          "Buy, add, trim, exit, and covered-call proposals must pass fresh broker and partition checks."])

story += chapter("Long Term actions in plain language", "PART 6 / INDEPENDENT PORTFOLIO")
story += [two_col([
              ["Action", "Meaning and beginner warning"],
              ["Buy / open", "Start a new long-term stock or LEAP position. Confirm the capital partition and maximum dollar commitment."],
              ["Add", "Increase an existing holding. Adding to a losing position increases risk; it does not repair the original decision."],
              ["Trim", "Sell part, but not all, of a holding. Verify the remaining shares or contracts after the fill."],
              ["Exit", "Close the entire selected long-term holding."],
              ["Covered call", "Sell a call against shares already owned. One contract normally obligates 100 shares and can cap upside."],
              ["Sector rotation", "Compare sector leadership and prepare research. Rankings are backward-looking observations, not assured future returns."],
          ]),
          section("Optional AI"),
          p("Long Term works with No AI. If OpenAI or Anthropic is selected, the subscriber supplies and pays for their own provider key. Ollama runs locally but uses disk, memory, CPU/GPU time, and electricity. AI output is research text, not permission to trade."),
          p("Never approve an order merely because an AI explanation sounds confident. Verify symbol, instrument, expiration, quantity, limit price, partition, buying power, and downside independently.", "Danger"), PageBreak()]

story += screenshot_page("My Results", "screen-results.jpg",
                         "My Results is the subscriber's local trading journal and summary.",
                         ["Review closed trades and realized outcomes.",
                          "Filter by strategy or symbol when comparing behavior.",
                          "Exported history is a record, not proof that a strategy will remain profitable.",
                          "Schwab remains the final source of truth for official orders, fills, balances, and tax documents."])

story += screenshot_page("System Map", "screen-system-map.jpg",
                         "System Map explains the boundaries: Andre publishes encrypted messages; this computer decrypts and controls its own Schwab account.",
                         ["Andre's side does not receive the subscriber's private key.",
                          "Only this device can open messages encrypted to its public key.",
                          "The local risk gate runs before a new entry.",
                          "The broker's response and position reconciliation are authoritative."])

story += chapter("Daily, weekly, and emergency routines", "PART 7 / OPERATIONS")
story += [section("Before the market each day"),
          bullets(["Start the copier and keep the computer awake.",
                   "Home: verify Signals from Andre is Connected.",
                   "Home: verify Schwab is Connected to the intended masked account.",
                   "Confirm Approve first unless automatic buying is intentionally enabled.",
                   "Review limits and active Signal Types.",
                   "Open Schwab separately and confirm buying power and existing positions."], numbered=True),
          section("Every week"),
          bullets(["Press Reconnect Schwab before the countdown expires.",
                   "Sign in on Schwab's site and approve access.",
                   "Confirm Home returns to Connected with roughly seven days remaining.",
                   "Install a newer copier build when the official page announces one; preserve the existing identity."], numbered=True),
          section("If something looks wrong"),
          bullets(["Stop approving new entries.", "Open Schwab Orders and Positions.",
                   "Close or reduce a real position directly if necessary.",
                   "Use Done for the day to block new entries.",
                   "Save a redacted screenshot and the agent.log file for support."], numbered=True),
          p("Closing the browser tab does not quit the copier. Use Quit Copier in the footer. Done for the day blocks new entries but keeps exits active.", "Warn"), PageBreak()]

story += chapter("Atomic multi-leg option groups", "PART 8 / SCHEMA V2")
story += [p(f"Version {VERSION} keeps every schema v1 single-contract workflow and adds schema v2 for complete two-leg and four-leg option position groups. A group is one risk-defined position. The copier never turns it into separate single-leg trades."),
          p("Current release boundary", "Section"),
          p("Schema-v2 <b>paper</b> signals are authenticated, validated, simulated, persisted, and displayed. They call zero broker methods. Live multi-leg signals are rejected because this build does not yet have independently proven Schwab native complex-order support. No leg is sent. Paper qualification is not evidence of profitability or live readiness.", "Warn"),
          two_col([["Badge", "Meaning"],
                   ["PAPER", "Complete group simulation only; the broker is never called."],
                   ["LIVE", "Would require entitlement, explicit live acknowledgement, account permission, exact contracts, and a proven native complex-order adapter. Currently rejected."],
                   ["schema v1", "Existing single stock or single option behavior remains unchanged."],
                   ["schema v2", "Two-leg vertical or four-leg iron structure; never downgraded to v1."]]),
          section("Safety rules that cannot be bypassed"),
          bullets(["No sequential legging and no market-order entry.",
                   "No expiry, strike, right, ratio, multiplier, or contract substitution.",
                   "A missing protective wing rejects the complete signal.",
                   "Unknown schema versions, structures, actions, or intents are recorded as rejected; nothing is guessed.",
                   "Stale, crossed, incomplete, expired, or economically inconsistent groups are rejected.",
                   "Duplicate event, signal, and group IDs cannot create a second group.",
                   "An ambiguous or partial live response would stop in UNCERTAIN and reconcile before any retry."]), PageBreak()]

story += chapter("Supported structures and leg map", "PART 8A / VISUAL GUIDE")
story += [p("Labels and action names matter more than color. Long/protective legs are marked BUY; short/premium legs are marked SELL."),
          two_col([["Structure", "Required strike geometry and opening legs"],
                   ["Bull-put credit vertical", "LOW: BUY_TO_OPEN long put  |  HIGH: SELL_TO_OPEN short put"],
                   ["Bear-call credit vertical", "LOW: SELL_TO_OPEN short call  |  HIGH: BUY_TO_OPEN long call"],
                   ["Bull-call debit vertical", "LOW: BUY_TO_OPEN long call  |  HIGH: SELL_TO_OPEN short call"],
                   ["Bear-put debit vertical", "LOW: SELL_TO_OPEN short put  |  HIGH: BUY_TO_OPEN long put"],
                   ["Iron condor", "long put < short put < short call < long call; all four legs required"],
                   ["Iron butterfly", "long put < shared short center < long call; both short rights at center"]], widths=(2.15 * inch, 4.35 * inch)),
          section("Two-leg diagram"),
          two_col([["LOWER STRIKE", "HIGHER STRIKE"],
                   ["BUY long protective put", "SELL short put"],
                   ["6395 PUT / BUY_TO_OPEN", "6400 PUT / SELL_TO_OPEN"]], widths=(3.25 * inch, 3.25 * inch)),
          p("BULL-PUT CREDIT VERTICAL: the lower long put is the protective wing. If either contract is missing, duplicated, or has the wrong expiry, the entire group is rejected.", "Warn"),
          section("Four-leg diagram"),
          two_col([["LONG PUT", "SHORT PUT  |  SHORT CALL  |  LONG CALL"],
                   ["BUY wing below", "SELL inner put  |  SELL inner call  |  BUY wing above"],
                   ["6390 P", "6395 P  <  6405 C  <  6410 C"]], widths=(2 * inch, 4.5 * inch)),
          p("IRON CONDOR: the strikes must remain in strict order and every leg must share the same underlying and expiry.", "Warn"), PageBreak()]

story += chapter("Net prices, actions, and risk display", "PART 8B / READ THE CARD")
story += [two_col([["Lifecycle", "Native group order", "Long-leg action", "Short-leg action"],
                   ["Credit open", "NET_CREDIT", "BUY_TO_OPEN", "SELL_TO_OPEN"],
                   ["Credit close", "NET_DEBIT", "SELL_TO_CLOSE", "BUY_TO_CLOSE"],
                   ["Debit open", "NET_DEBIT", "BUY_TO_OPEN", "SELL_TO_OPEN"],
                   ["Debit close", "NET_CREDIT", "SELL_TO_CLOSE", "BUY_TO_CLOSE"]], widths=(1.25 * inch, 1.4 * inch, 1.9 * inch, 1.9 * inch)),
          p("All net prices are positive USD-per-share magnitudes. Option cash equals net price x multiplier x group quantity. A negative or zero limit is invalid; the copier never infers debit or credit from a sign."),
          section("What the group card shows"),
          bullets(["Strategy, underlying, structure, expiry, PAPER/LIVE badge, and group state.",
                   "Every OCC contract, option right, strike, open/close action, ratio, and leg status.",
                   "Group quantity, NET_CREDIT or NET_DEBIT limit, multiplier, and quote age.",
                   "Maximum gain, maximum loss, and buying-power reservation recomputed from the structure.",
                   "Forced-exit time, settlement warning, and durable rejection or reconciliation detail."], numbered=True),
          p("Maximum gain and loss are per complete group. Quantity multiplies the complete structure. Never multiply only one leg when checking exposure.", "Danger"), PageBreak()]

story += chapter("Multi-leg workflow and status runbook", "PART 8C / OPERATE SAFELY")
story += [bullets(["Publisher creates an explicit schema-v2 group; it does not pass through v1 normalization.",
                   "Publisher filters by strategy entitlement and explicit schema-v2 paper capability.",
                   "Subscriber verifies the signature, decrypts, claims the event idempotently, and validates the complete structure.",
                   "Paper mode simulates and stores every leg in one transaction, then shows one group card.",
                   "A group exit closes the verified complete paper group. No per-leg buttons are offered."], numbered=True),
          two_col([["State", "Meaning and trader action"],
                   ["PENDING_APPROVAL", "Complete group is waiting for a deliberate review; approving applies to the group."],
                   ["OPENING", "One native complex order would be in progress. Do not submit another."],
                   ["OPEN", "Complete group is held and monitored as one position."],
                   ["CLOSING", "Whole-group closing order is in progress."],
                   ["CLOSED", "All verified group quantity is closed."],
                   ["REJECTED", "Nothing was traded; read the human-readable reason."],
                   ["PARTIAL_UNWIND", "A partial-fill recovery is underway; do not add exposure."],
                   ["UNCERTAIN", "Stop. Inspect Schwab orders and positions; never retry or trade an individual leg."]]),
          section("Common rejection and recovery cases"),
          bullets(["Unsupported account or permissions: no order; confirm complex-options approval with the broker.",
                   "Unresolved exact contract or missing wing: reject the complete group.",
                   "Stale/crossed quote or expired event: reject; do not refresh into a different trade.",
                   "Buying-power or risk mismatch: reject; reduce risk at the source rather than deleting a wing.",
                   "Duplicate event: show the prior outcome; never submit twice.",
                   "Position mismatch or ambiguous submission: mark UNCERTAIN and reconcile against broker truth.",
                   "Restart during a transitional live state: recover open orders, order history, and holdings before processing another event.",
                   "Missed forced exit: treat as an emergency; inspect and close the complete verified group in Schwab."]), PageBreak()]

story += chapter("Troubleshooting", "PART 9 / FIX COMMON PROBLEMS")
story += [two_col([
              ["What you see", "What to do"],
              ["Waiting for Andre", "Leave it open for one minute. Andre must link the exact current TV1- code and send the private connection check. Do not create another identity during an update."],
              ["Connected but button still says Connect Schwab", "Trust the green connected status. The button is available for reconnection. Continue to the next setup step or Home."],
              ["Trying to connect / zero checks", "Verify internet access and that the copier process is still running. It retries every 20 seconds."],
              ["No new signal", "First confirm the private connection check. Then remember: only a new live filled short-term trade is eligible. Paper and Long Term activity are ignored."],
              ["Schwab expired", "Reconnect immediately. Inspect Schwab directly if a position is open."],
              ["Uncertain order", "Do not retry. Inspect Schwab Orders and Positions first."],
              ["Mac SSL time warning", "Update macOS and certificates, enable automatic Date & Time, restart, and do not rely on a custom hours window until the warning clears."],
              ["PowerShell window flashes", "Install the current packaged build and use its shortcut. Quit older copier processes so scheduled or legacy launchers are not competing."],
              ["Mac bad CPU type", "Delete the file and download the other Mac architecture."],
              ["No such file", "Check Downloads and remove a (1) filename suffix by downloading once cleanly."],
          ]),
          p("If a real position is open and the app is confusing, Schwab is the source of truth. Protect the account first; troubleshoot second.", "Danger"), PageBreak()]

story += chapter("Glossary", "PART 10 / QUICK REFERENCE")
story += [two_col([
              ["Word", "Meaning"],
              ["0DTE", "An option expiring today. It can move or lose value extremely quickly."],
              ["Buying power", "The broker's estimate of funds available for new positions."],
              ["Callback URL", "The local address Schwab returns to after authorization."],
              ["Covered call", "A short call backed by enough owned shares, normally 100 shares per contract."],
              ["Device code", "The safe-to-share TV1- code containing a device ID and public key."],
              ["Fill", "Broker confirmation that an order executed."],
              ["Limit order", "An order that will not pay above or sell below a specified price, but may never fill."],
              ["Long / short", "Long generally benefits from a rise; short or bearish exposure generally benefits from a fall."],
              ["Premium", "The price of an option; standard quotes are per share, normally multiplied by 100."],
              ["R", "The planned loss distance from entry to stop."],
              ["Slippage", "The difference between expected and actual fill price."],
              ["Stop", "A planned loss exit. Fast markets can fill worse than the stop level."],
              ["Strategy", "A repeatable set of conditions for setup, entry, stop, and exit."],
              ["TV1- code", "The copier's public connection code. It is not the private key."],
              ["VWAP", "Volume-weighted average price, a common intraday reference line."],
          ]), PageBreak()]

story += chapter("Security and support checklist", "APPENDIX")
story += [section("Never share"),
          bullets(["Schwab username or password", "Schwab App Secret",
                   "OAuth callback authorization code or refresh authorization",
                   "The copier private key or secrets.json fallback",
                   "Remote-control access while Schwab is open"]),
          section("Safe to share for support"),
          bullets(["The complete TV1- public device code",
                   "A screenshot with account numbers, balances, keys, and personal information redacted",
                   "agent.log when specifically requested and reviewed for sensitive information"]),
          section("Local storage"),
          p("Windows: C:\\Users\\&lt;you&gt;\\.trading-copier\\<br/>macOS: ~/.trading-copier/", "CodeX"),
          p("This folder preserves identity and settings across normal upgrades. Back it up securely. Do not email it."),
          Spacer(1, .2 * inch),
          p(f"Trading Copier Installation Guide and User Manual. Revised 15 August 2026 for version {VERSION}, application schema v1 and multi-leg schema v2. Source: build_user_manual.py. The software and this document are provided as-is, without warranty. Nothing here is investment advice. Trading involves risk of loss.", "Small"),
          p("Copyright 2026 Walkers Software LLC. All rights reserved.", "Small")]

story += [PageBreak()] + chapter("Authoritative investor references", "APPENDIX")
story += [p("The strategy chapters describe the copier's own current rules. For general securities and options education, use these independent regulator and broker resources:"),
          bullets(["SEC Investor.gov - An Introduction to Options:<br/>https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-63",
                   "FINRA - Options:<br/>https://www.finra.org/investors/investing/investment-products/options",
                   "FINRA - Order Types:<br/>https://www.finra.org/investors/investing/investment-products/stocks/order-types",
                   "FINRA - Stop Orders in Volatile Markets:<br/>https://www.finra.org/investors/insights/stop-orders-factors-consider-during-volatile-markets",
                   "Charles Schwab - Basic Call and Put Options Strategies:<br/>https://www.schwab.com/learn/story/basic-call-and-put-options-strategies"]),
          p("Read the current Characteristics and Risks of Standardized Options disclosure supplied by the broker before trading options. Provider pages, costs, approval rules, and product availability can change; the linked official source wins over this manual.", "Warn")]


ManualDoc(str(OUT)).multiBuild(story)
print(OUT)
