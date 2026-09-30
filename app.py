import gradio as gr
import time
from datetime import datetime

from receipt_parser import extract_receipt
from agent import ask_agent as run_agent


def format_purchase_date(date_value):
    """Display receipt dates as DD/MM/YYYY without changing the stored value."""
    if not date_value:
        return date_value

    date_text = str(date_value).strip()
    for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_text, fmt).strftime("%d/%m/%Y")
        except ValueError:
            pass

    return date_text


# ============================================================
# PROCESS RECEIPT
# ============================================================

def processing_status(title, detail):
    return f"""
<div class="processing-status">
    <div class="processing-spinner"></div>
    <div>
        <div class="processing-title">{title}</div>
        <div class="processing-detail">{detail}</div>
    </div>
</div>
"""


def process_receipt(pdf_file, question):

    if pdf_file is None:
        yield (
            "Please upload a receipt PDF.",
            "",
            question or "",
            "",
            ""
        )
        return

    if not question or not question.strip():
        yield (
            "Please enter a question.",
            "",
            "",
            "",
            ""
        )
        return

    try:
        # ----------------------------------------------------
        # STEP 1 — Start processing
        # ----------------------------------------------------

        yield (
            processing_status(
                "Analyzing your receipt...",
                "Reading the uploaded PDF and preparing the receipt data."
            ),
            "",
            question,
            "### Agent is working\n\nPlease wait while Receipt Agent processes your request.",
            ""
        )

        time.sleep(0.35)

        # ----------------------------------------------------
        # STEP 2 — Extract receipt information
        # ----------------------------------------------------

        receipt = extract_receipt(pdf_file)

        order_id = receipt["order_id"]
        product = receipt["product"]
        purchase_date = receipt["purchase_date"]
        display_purchase_date = format_purchase_date(purchase_date)

        if not order_id:
            yield (
                "I couldn't find an Order ID in this receipt.",
                "",
                question,
                "",
                "Processing stopped"
            )
            return

        receipt_info = f"""
<div class="receipt-cards">
    <div class="info-card">
        <div class="info-label">ORDER ID</div>
        <div class="info-value mono">{order_id}</div>
        <div class="info-line"></div>
    </div>
    <div class="info-card">
        <div class="info-label">PRODUCT</div>
        <div class="info-value">{product}</div>
        <div class="info-line"></div>
    </div>
    <div class="info-card">
        <div class="info-label">PURCHASE DATE</div>
        <div class="info-value">{display_purchase_date}</div>
        <div class="info-line"></div>
    </div>
</div>
<div class="verified-status">
    <span class="verified-dot"></span>
    <span><strong>ORDER VERIFIED</strong><small>Receipt successfully identified</small></span>
</div>
"""

        yield (
            processing_status(
                "Receipt identified",
                f"Order {order_id} found successfully."
            ),
            receipt_info,
            question,
            "### Agent is working\n\nReceipt extracted. Preparing your answer...",
            f"Order `{order_id}`"
        )

        time.sleep(0.35)

        # ----------------------------------------------------
        # STEP 3 — Prepare agent request
        # ----------------------------------------------------

        agent_question = f"""
The user uploaded a receipt.

Receipt information:
Order ID: {order_id}
Product: {product}
Purchase Date: {purchase_date}

User's question:
{question}

Use the Order ID to look up the order.

Use the available policy and deadline tools when necessary.

Do not invent information that is not provided by the
order database or store policy.
"""

        yield (
            processing_status(
                "Checking your order...",
                "Looking up order information and relevant store policies."
            ),
            receipt_info,
            question,
            "### Checking order information\n\nSearching the connected tools and policies...",
            f"Order `{order_id}`"
        )

        # ----------------------------------------------------
        # STEP 4 — Ask agent
        # ----------------------------------------------------

        response = run_agent(agent_question)

        # ----------------------------------------------------
        # STEP 5 — Final answer
        # ----------------------------------------------------

        yield (
            "Receipt processed successfully",
            receipt_info,
            question,
            response.content,
            f"Order `{order_id}`"
        )

    except Exception as e:

        print("\n========== APPLICATION ERROR ==========")
        print(e)
        print("=======================================\n")

        yield (
            "Something went wrong while processing the receipt.",
            "",
            question,
            f"**Error:** `{str(e)}`",
            "Processing failed"
        )


# ============================================================
# CUSTOM CSS
# ============================================================

custom_css = """

/* =========================================================
PAGE
========================================================= */

body {

background:
    radial-gradient(
        circle at 10% 10%,
        rgba(99, 102, 241, 0.16),
        transparent 30%
    ),
    radial-gradient(
        circle at 90% 20%,
        rgba(168, 85, 247, 0.14),
        transparent 30%
    ),
    linear-gradient(
        135deg,
        #080b16,
        #101426,
        #080b16
    );

color: #f8fafc;

}

/* =========================================================
VISIBLE ANIMATED SPACE BACKGROUND
========================================================= */

html, body {
    min-height: 100% !important;
    background: #020617 !important;
}

body {
    overflow-x: hidden !important;
}

/* The Gradio page itself must stay transparent so the animation can be seen. */
.gradio-container {
    position: relative !important;
    z-index: 1 !important;
    background: transparent !important;
    max-width: 1250px !important;
    margin: auto !important;
}

.background-layer {
    position: static !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    pointer-events: none !important;
}


.space-background,
.wave-background {
    position: fixed !important;
    inset: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    pointer-events: none !important;
    overflow: hidden !important;
    transition: opacity 1.1s ease, transform 1.2s ease !important;
}

.space-background {
    z-index: 0 !important;
    opacity: 1;
    background:
        radial-gradient(circle at 12% 18%, rgba(56,189,248,.15), transparent 22%),
        radial-gradient(circle at 88% 20%, rgba(192,132,252,.15), transparent 24%),
        radial-gradient(circle at 50% 85%, rgba(59,130,246,.10), transparent 30%),
        linear-gradient(135deg, #010617 0%, #050a20 48%, #10051d 100%);
}

.space-background::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(circle, rgba(255,255,255,.95) 0 1px, transparent 1.8px),
        radial-gradient(circle, rgba(96,165,250,.80) 0 1.2px, transparent 2px),
        radial-gradient(circle, rgba(216,180,254,.75) 0 1px, transparent 1.8px);
    background-size: 105px 105px, 165px 165px, 230px 230px;
    background-position: 20px 10px, 60px 80px, 120px 35px;
    animation: starFieldMove 22s linear infinite;
    opacity: .55;
}

.space-background::after {
    content: "";
    position: absolute;
    inset: -10%;
    background:
        radial-gradient(ellipse at center, transparent 42%, rgba(0,0,0,.45) 100%),
        linear-gradient(115deg, transparent 0 48%, rgba(129,140,248,.035) 50%, transparent 52%);
}

.shooting-star {
    position: absolute !important;
    display: block !important;
    width: 180px;
    height: 3px;
    border-radius: 999px;
    opacity: 0;
    transform: rotate(-32deg);
    filter: drop-shadow(0 0 7px currentColor) drop-shadow(0 0 16px currentColor);
    animation: meteorFly 4.8s linear infinite !important;
}

.shooting-star::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    width: 9px;
    height: 9px;
    transform: translate(-3px,-50%);
    border-radius: 50%;
    background: #fff;
    box-shadow: 0 0 8px currentColor, 0 0 20px currentColor, 0 0 35px currentColor;
}

.shooting-star::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(90deg, currentColor 0%, rgba(255,255,255,.95) 12%, currentColor 38%, transparent 100%);
}

.shooting-star:nth-child(1)  { left: -12%; top: 12%; color:#22d3ee; animation-delay: 0s !important; }
.shooting-star:nth-child(2)  { left: 18%;  top: 8%;  color:#c084fc; animation-delay: 1.1s !important; transform: rotate(-32deg) scale(.70); }
.shooting-star:nth-child(3)  { left: 54%;  top: 16%; color:#60a5fa; animation-delay: 2.2s !important; transform: rotate(-32deg) scale(.58); }
.shooting-star:nth-child(4)  { left: 86%;  top: 25%; color:#e879f9; animation-delay: 3.0s !important; transform: rotate(-32deg) scale(.78); }
.shooting-star:nth-child(5)  { left: -8%;  top: 42%; color:#818cf8; animation-delay: 3.8s !important; transform: rotate(-32deg) scale(.62); }
.shooting-star:nth-child(6)  { left: 40%;  top: 48%; color:#22d3ee; animation-delay: .7s !important; transform: rotate(-32deg) scale(.68); }
.shooting-star:nth-child(7)  { left: 76%;  top: 56%; color:#a78bfa; animation-delay: 2.8s !important; transform: rotate(-32deg) scale(.55); }
.shooting-star:nth-child(8)  { left: 22%;  top: 70%; color:#38bdf8; animation-delay: 4.1s !important; transform: rotate(-32deg) scale(.74); }
.shooting-star:nth-child(9)  { left: 91%;  top: 76%; color:#d946ef; animation-delay: 1.8s !important; transform: rotate(-32deg) scale(.64); }
.shooting-star:nth-child(10) { left: 3%;   top: 88%; color:#818cf8; animation-delay: 4.6s !important; transform: rotate(-32deg) scale(.50); }

@keyframes meteorFly {
    /* START: top-right */
    0% {
        opacity: 0;
        transform: translate3d(78vw,-18vh,0) rotate(-32deg) scale(.65);
    }
    7% { opacity: 1; }
    25% { opacity: 1; }
    /* END: bottom-left */
    43% {
        opacity: 0;
        transform: translate3d(-18vw,112vh,0) rotate(-32deg) scale(1);
    }
    100% {
        opacity: 0;
        transform: translate3d(-18vw,112vh,0) rotate(-32deg) scale(1);
    }
}

@keyframes starFieldMove {
    from { transform: translate3d(0,0,0); }
    to   { transform: translate3d(-90px,65px,0); }
}

/* =========================================================
SECOND SCENE — NEON WAVES
========================================================= */

.wave-background {
    z-index: 0 !important;
    opacity: 0;
    transform: scale(1.04);
    background:
        radial-gradient(circle at 18% 82%, rgba(34,211,238,.16), transparent 26%),
        radial-gradient(circle at 82% 78%, rgba(217,70,239,.15), transparent 27%),
        linear-gradient(160deg, #020617 0%, #07051b 48%, #12051f 100%);
}

.wave-background::before,
.wave-background::after {
    content: "";
    position: absolute;
    left: -12%;
    width: 124%;
    height: 38%;
    bottom: 4%;
    border-radius: 50%;
    border: 3px solid rgba(56,189,248,.48);
    box-shadow: 0 0 18px rgba(56,189,248,.35), 0 0 55px rgba(56,189,248,.15);
    transform: rotate(-5deg) translateX(-4%);
    animation: neonWave 6s ease-in-out infinite alternate;
}

.wave-background::after {
    bottom: -2%;
    border-color: rgba(217,70,239,.46);
    box-shadow: 0 0 18px rgba(217,70,239,.35), 0 0 60px rgba(168,85,247,.16);
    transform: rotate(5deg) translateX(5%);
    animation-duration: 8s;
    animation-direction: alternate-reverse;
}

.wave-line {
    position: absolute;
    left: -10%;
    width: 120%;
    height: 180px;
    bottom: 16%;
    border-top: 2px solid rgba(129,140,248,.30);
    border-radius: 50%;
    transform: rotate(-2deg);
    animation: neonWave2 7s ease-in-out infinite alternate;
}

@keyframes neonWave {
    from { transform: rotate(-5deg) translate3d(-4%,0,0) scaleY(.88); }
    to   { transform: rotate(-5deg) translate3d(4%,-18px,0) scaleY(1.08); }
}

@keyframes neonWave2 {
    from { transform: rotate(-2deg) translateX(-3%); }
    to   { transform: rotate(-2deg) translateX(5%) translateY(-15px); }
}

/* JavaScript adds .show-waves when the user scrolls down. */
body.show-waves .space-background {
    opacity: .12 !important;
    transform: scale(1.03);
}

body.show-waves .wave-background {
    opacity: 1 !important;
    transform: scale(1) !important;
}

/* Keep the actual application above both background layers. */
.gradio-container > *:not(.background-layer) {
    position: relative;
    z-index: 2;
}

/* =========================================================
MAIN CONTAINER
========================================================= */


========================================================= */

.gradio-container {

max-width: 1250px !important;

margin: auto !important;

padding: 25px !important;

}

/* =========================================================
HERO
========================================================= */

.hero {

padding: 45px 35px;

margin-bottom: 25px;

border-radius: 24px;

background:
    linear-gradient(
        135deg,
        rgba(30, 41, 59, 0.95),
        rgba(15, 23, 42, 0.90)
    );

border:
    1px solid rgba(255,255,255,0.08);

box-shadow:
    0 25px 70px rgba(0,0,0,0.45);

text-align: center;

animation:
    heroAppear 0.8s ease;

}

/* HERO ANIMATION */

@keyframes heroAppear {

from {

    opacity: 0;

    transform:
        translateY(-15px);

}

to {

    opacity: 1;

    transform:
        translateY(0);

}

}

/* =========================================================
HERO ICON
========================================================= */

.hero-icon {

font-size: 52px;

margin-bottom: 10px;

display: inline-block;

animation:
    floatingIcon 3s ease-in-out infinite;

}

/* ICON FLOAT */

@keyframes floatingIcon {

0%,
100% {

    transform:
        translateY(0);

}

50% {

    transform:
        translateY(-8px);

}

}

/* =========================================================
HERO TITLE
========================================================= */

.hero-title {

font-size: 42px;

font-weight: 800;

background:
    linear-gradient(
        90deg,
        #ffffff,
        #a5b4fc,
        #c084fc,
        #ffffff
    );

background-size: 200% auto;

-webkit-background-clip: text;

-webkit-text-fill-color: transparent;

animation:
    titleGlow 5s linear infinite;

margin-bottom: 10px;

}

/* TITLE ANIMATION */

@keyframes titleGlow {

0% {

    background-position:
        0% center;

}

100% {

    background-position:
        200% center;

}

}

/* =========================================================
HERO SUBTITLE
========================================================= */

.hero-subtitle {

color: #94a3b8;

font-size: 17px;

max-width: 700px;

margin: auto;

line-height: 1.7;

}

/* =========================================================
STATUS CARDS
========================================================= */

.status-card {

padding: 14px 18px;

border-radius: 14px;

background:
    rgba(15,23,42,0.75);

border:
    1px solid rgba(255,255,255,0.08);

color: #cbd5e1;

font-weight: 600;

text-align: center;

transition:
    all 0.25s ease;

}

/* STATUS HOVER */

.status-card:hover {

transform:
    translateY(-3px);

border-color:
    rgba(129,140,248,0.45);

box-shadow:
    0 10px 30px rgba(99,102,241,0.15);

}

/* =========================================================
PANELS
========================================================= */

.panel {

background:
    rgba(15, 23, 42, 0.78) !important;

border:
    1px solid rgba(255,255,255,0.08) !important;

border-radius:
    20px !important;

padding:
    22px !important;

box-shadow:
    0 15px 45px rgba(0,0,0,0.25);

backdrop-filter:
    blur(12px);

transition:
    transform 0.25s ease,
    border-color 0.25s ease,
    box-shadow 0.25s ease;

}

/* PANEL HOVER */

.panel:hover {

border-color:
    rgba(129,140,248,0.20) !important;

box-shadow:
    0 20px 55px rgba(0,0,0,0.30);

}

/* =========================================================
SECTION TITLES
========================================================= */

.section-title {

font-size: 18px;

font-weight: 700;

color: #e2e8f0;

margin-bottom: 12px;

}

/* =========================================================
UPLOAD BOX
========================================================= */

.upload-box {

border:
    1px dashed rgba(129,140,248,0.55);

border-radius: 18px;

background:
    rgba(99,102,241,0.05);

padding: 12px;

transition:
    all 0.3s ease;

}

/* UPLOAD HOVER */

.upload-box:hover {

border-color:
    rgba(167,139,250,0.9);

background:
    rgba(99,102,241,0.10);

transform:
    translateY(-2px);

box-shadow:
    0 10px 30px rgba(99,102,241,0.10);

}

/* =========================================================
INPUT
========================================================= */

textarea,
input {

border-radius:
    12px !important;

border:
    1px solid rgba(255,255,255,0.10) !important;

background:
    rgba(15,23,42,0.85) !important;

color:
    #f8fafc !important;

transition:
    border-color 0.25s ease,
    box-shadow 0.25s ease;

}

/* INPUT FOCUS */

textarea:focus,
input:focus {

border-color:
    rgba(129,140,248,0.65) !important;

box-shadow:
    0 0 0 3px rgba(99,102,241,0.12) !important;

}

/* =========================================================
ASK BUTTON
========================================================= */

.ask-button {

border-radius:
    14px !important;

border:
    none !important;

background:
    linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    ) !important;

color:
    white !important;

font-size:
    16px !important;

font-weight:
    700 !important;

padding:
    15px !important;

box-shadow:
    0 10px 30px rgba(99,102,241,0.35);

transition:
    transform 0.18s ease,
    box-shadow 0.25s ease,
    filter 0.25s ease;

}

/* ASK BUTTON HOVER */

.ask-button:hover {

transform:
    translateY(-3px);

box-shadow:
    0 16px 40px rgba(139,92,246,0.45);

filter:
    brightness(1.08);

}

/* ASK BUTTON CLICK */

.ask-button:active {

transform:
    translateY(1px)
    scale(0.97);

box-shadow:
    0 6px 18px rgba(99,102,241,0.30);

}

/* =========================================================
QUICK BUTTONS
========================================================= */

.quick-title {

color:
    #94a3b8;

font-size:
    13px;

font-weight:
    600;

margin-top:
    8px;

}

/* QUICK BUTTON */

.quick-button {

border-radius:
    12px !important;

border:
    1px solid rgba(255,255,255,0.08) !important;

background:
    rgba(30,41,59,0.65) !important;

color:
    #cbd5e1 !important;

transition:
    all 0.2s ease;

}

/* QUICK BUTTON HOVER */

.quick-button:hover {

transform:
    translateY(-2px);

background:
    rgba(99,102,241,0.18) !important;

border-color:
    rgba(129,140,248,0.45) !important;

box-shadow:
    0 8px 20px rgba(99,102,241,0.12);

}

/* QUICK BUTTON CLICK */

.quick-button:active {

transform:
    scale(0.95);

}

/* =========================================================
ANSWER BOX
========================================================= */

.answer-box {

border-radius:
    18px !important;

background:
    linear-gradient(
        135deg,
        rgba(30,41,59,0.90),
        rgba(15,23,42,0.90)
    ) !important;

border:
    1px solid rgba(129,140,248,0.20) !important;

animation:
    answerAppear 0.5s ease;

}

/* ANSWER ANIMATION */

@keyframes answerAppear {

from {

    opacity: 0;

    transform:
        translateY(10px);

}

to {

    opacity: 1;

    transform:
        translateY(0);

}

}

/* =========================================================
RECEIPT BOX
========================================================= */

.receipt-box {

border-radius:
    16px;

background:
    rgba(30,41,59,0.65);

border:
    1px solid rgba(255,255,255,0.07);

padding:
    18px;

}

/* =========================================================
AGENT RESPONSE — DISTINCT CONVERSATIONAL CARD
========================================================= */

.answer-box {
    position: relative;
    overflow: hidden;
    padding: 24px !important;
    border-radius: 20px !important;
    background:
        radial-gradient(circle at 100% 0%, rgba(129,140,248,0.14), transparent 32%),
        linear-gradient(145deg, rgba(15,23,42,0.96), rgba(30,41,59,0.88)) !important;
    border: 1px solid rgba(148,163,184,0.13) !important;
    box-shadow: 0 18px 50px rgba(0,0,0,0.28);
    transition: transform .3s ease, border-color .3s ease, box-shadow .3s ease;
}

.answer-box::before {
    content: "AGENT INSIGHT";
    display: inline-flex;
    align-items: center;
    gap: 7px;
    margin-bottom: 14px;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(129,140,248,0.22);
    color: #a5b4fc;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.answer-box::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 3px;
    height: 100%;
    background: linear-gradient(180deg, #818cf8, #c084fc, transparent);
    animation: responseEdge 2.8s ease-in-out infinite;
}

.answer-box:hover {
    transform: translateY(-3px);
    border-color: rgba(129,140,248,0.30) !important;
    box-shadow: 0 24px 65px rgba(79,70,229,0.16);
}

.answer-box h3,
.answer-box h4 {
    color: #f8fafc !important;
    margin-top: 4px;
}

.answer-box p {
    color: #cbd5e1;
    line-height: 1.75;
}

.answer-box strong {
    color: #eef2ff;
}

.answer-box blockquote {
    margin: 16px 0;
    padding: 13px 16px;
    border-left: 3px solid #818cf8;
    border-radius: 0 12px 12px 0;
    background: rgba(99,102,241,0.07);
    color: #cbd5e1;
}

@keyframes responseEdge {
    0%,100% { opacity: .45; transform: scaleY(.72); transform-origin: top; }
    50% { opacity: 1; transform: scaleY(1); transform-origin: center; }
}

/* small animated status beneath the answer */
.agent-status {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 14px;
    color: #94a3b8;
    font-size: 12px;
}

.agent-status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #818cf8;
    box-shadow: 0 0 0 0 rgba(129,140,248,.55);
    animation: agentDot 1.8s infinite;
}

@keyframes agentDot {
    0% { box-shadow: 0 0 0 0 rgba(129,140,248,.5); }
    70% { box-shadow: 0 0 0 7px rgba(129,140,248,0); }
    100% { box-shadow: 0 0 0 0 rgba(129,140,248,0); }
}


/* =========================================================
UPLOAD RECEIPT — INTELLIGENT DROP ZONE
========================================================= */

.upload-panel {
    position: relative;
    overflow: hidden;
}

.upload-panel::before {
    content: "";
    position: absolute;
    top: 0;
    left: 8%;
    right: 8%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(129,140,248,.75), rgba(192,132,252,.65), transparent);
    animation: uploadGlow 3.8s ease-in-out infinite;
}

.upload-panel::after {
    content: "";
    position: absolute;
    width: 150px;
    height: 150px;
    right: -90px;
    top: -95px;
    border-radius: 50%;
    background: rgba(129,140,248,.08);
    filter: blur(8px);
    pointer-events: none;
}

.upload-intro {
    display: flex;
    align-items: center;
    gap: 13px;
    margin: 4px 0 15px;
}

.upload-orb {
    position: relative;
    width: 42px;
    height: 42px;
    flex: 0 0 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    background: linear-gradient(145deg, rgba(99,102,241,.22), rgba(192,132,252,.14));
    border: 1px solid rgba(129,140,248,.25);
    box-shadow: 0 8px 24px rgba(79,70,229,.12);
}

.upload-orb::before {
    content: "";
    position: absolute;
    inset: -5px;
    border-radius: 18px;
    border: 1px solid rgba(129,140,248,.16);
    animation: uploadPulse 2.4s ease-in-out infinite;
}

.upload-orb svg {
    width: 21px;
    height: 21px;
    fill: none;
    stroke: #c7d2fe;
    stroke-width: 1.8;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.upload-copy-title {
    color: #f8fafc;
    font-size: 13px;
    font-weight: 750;
}

.upload-copy-subtitle {
    color: #64748b;
    font-size: 11px;
    margin-top: 3px;
}

.upload-hints {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 13px;
}

.upload-hint {
    padding: 9px 8px;
    border-radius: 11px;
    text-align: center;
    background: rgba(15,23,42,.58);
    border: 1px solid rgba(255,255,255,.055);
    color: #94a3b8;
    font-size: 10px;
    transition: transform .25s ease, border-color .25s ease, background .25s ease;
}

.upload-hint:hover {
    transform: translateY(-2px);
    border-color: rgba(129,140,248,.24);
    background: rgba(99,102,241,.07);
}

.upload-hint strong {
    display: block;
    color: #cbd5e1;
    font-size: 11px;
    margin-bottom: 2px;
}

@keyframes uploadGlow {
    0%, 100% { opacity: .35; transform: scaleX(.75); }
    50% { opacity: 1; transform: scaleX(1); }
}

@keyframes uploadPulse {
    0%, 100% { opacity: .25; transform: scale(.94); }
    50% { opacity: .8; transform: scale(1.04); }
}

@media (max-width: 700px) {
    .upload-hints { grid-template-columns: 1fr; }
}

/* =========================================================
MARKDOWN
========================================================= */

.markdown-text {

color:
    #e2e8f0;

}

/* =========================================================
FOOTER
========================================================= */

.footer {

text-align:
    center;

margin-top:
    25px;

padding:
    20px;

color:
    #64748b;

font-size:
    13px;

}

/* =========================================================
HIDE GRADIO FOOTER
========================================================= */

footer {

display:
    none !important;

}

/* =========================================================
MODERN ICONS + MICRO ANIMATIONS
========================================================= */

.hero-icon svg { width: 52px; height: 52px; fill: none; stroke: #e0e7ff; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; filter: drop-shadow(0 8px 18px rgba(129,140,248,0.28)); }

.ui-icon { width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; flex: 0 0 24px; }
.ui-icon svg { width: 22px; height: 22px; fill: none; stroke: #c7d2fe; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.section-title { display: flex; align-items: center; gap: 9px; }

.status-card { position: relative; overflow: hidden; }
.status-card::after { content: ""; position: absolute; top: 0; left: -120%; width: 70%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.10), transparent); transform: skewX(-18deg); animation: statusSweep 5s ease-in-out infinite; }
@keyframes statusSweep { 0%,55% { left: -120%; } 80%,100% { left: 150%; } }

.upload-box { position: relative; overflow: hidden; }
.upload-box::after { content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none; box-shadow: inset 0 0 0 1px rgba(129,140,248,0); transition: box-shadow .3s ease; }
.upload-box:hover::after { box-shadow: inset 0 0 25px rgba(99,102,241,0.10); }

.ask-button { position: relative; overflow: hidden; }
.ask-button::after { content: ""; position: absolute; top: 0; left: -80%; width: 45%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.22), transparent); transform: skewX(-20deg); animation: buttonShine 3.5s ease-in-out infinite; }
@keyframes buttonShine { 0%,60% { left: -80%; } 85%,100% { left: 150%; } }

@keyframes answerPulse { 0%,100% { box-shadow: 0 15px 45px rgba(0,0,0,0.25); } 50% { box-shadow: 0 18px 55px rgba(99,102,241,0.16); } }
.panel:hover .answer-box { animation: answerPulse 2.5s ease-in-out infinite; }

/* =========================================================
RECEIPT INTELLIGENCE CARDS
========================================================= */

.receipt-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 14px 0 12px;
}

.info-card {
    position: relative;
    overflow: hidden;
    min-height: 105px;
    padding: 16px;
    border-radius: 16px;
    background: linear-gradient(145deg, rgba(30,41,59,0.92), rgba(15,23,42,0.82));
    border: 1px solid rgba(129,140,248,0.16);
    box-shadow: 0 10px 28px rgba(0,0,0,0.18);
    animation: infoCardAppear 0.5s ease both;
    transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
}

.info-card:nth-child(2) { animation-delay: .08s; }
.info-card:nth-child(3) { animation-delay: .16s; }

.info-card:hover {
    transform: translateY(-4px);
    border-color: rgba(167,139,250,0.45);
    box-shadow: 0 16px 35px rgba(99,102,241,0.16);
}

.info-card::before {
    content: "";
    position: absolute;
    width: 90px;
    height: 90px;
    right: -35px;
    top: -45px;
    border-radius: 50%;
    background: rgba(129,140,248,0.10);
    filter: blur(3px);
}

.info-label {
    color: #818cf8;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin-bottom: 10px;
}

.info-value {
    position: relative;
    color: #f8fafc;
    font-size: 14px;
    font-weight: 650;
    line-height: 1.45;
    word-break: break-word;
}

.info-value.mono {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 13px;
}

.info-line {
    width: 34px;
    height: 3px;
    margin-top: 13px;
    border-radius: 99px;
    background: linear-gradient(90deg, #6366f1, #c084fc);
}

.verified-status {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 12px 15px;
    border-radius: 14px;
    background: rgba(34,197,94,0.07);
    border: 1px solid rgba(74,222,128,0.18);
    animation: verifiedAppear .55s ease .2s both;
}

.verified-status strong {
    display: block;
    color: #bbf7d0;
    font-size: 11px;
    letter-spacing: .9px;
}

.verified-status small {
    display: block;
    color: #86efac;
    opacity: .72;
    font-size: 11px;
    margin-top: 2px;
}

.verified-dot {
    width: 10px;
    height: 10px;
    flex: 0 0 10px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 0 5px rgba(74,222,128,0.10), 0 0 16px rgba(74,222,128,0.55);
    animation: verifiedPulse 1.8s ease-in-out infinite;
}

@keyframes infoCardAppear {
    from { opacity: 0; transform: translateY(12px) scale(.98); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes verifiedAppear {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes verifiedPulse {
    0%, 100% { box-shadow: 0 0 0 5px rgba(74,222,128,0.10), 0 0 16px rgba(74,222,128,0.35); }
    50% { box-shadow: 0 0 0 8px rgba(74,222,128,0.04), 0 0 22px rgba(74,222,128,0.65); }
}

/* =========================================================
MOBILE
========================================================= */

@media (max-width: 700px) {

.hero-title {

    font-size:
        30px;

}

.hero {

    padding:
        30px 20px;

}

.hero-subtitle {

    font-size:
        14px;

}

.gradio-container {

    padding:
        12px !important;

}

}

@media (max-width: 700px) {
    .receipt-cards { grid-template-columns: 1fr; }
    .info-card { min-height: auto; }
}

/* =========================================================
REDUCED MOTION
========================================================= */

@media (prefers-reduced-motion: reduce) {

* {

    animation:
        none !important;

    transition:
        none !important;

}

}


/* =========================================================
PROCESSING / LOADING STATE
========================================================= */

.processing-status {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 16px;
    margin: 4px 0;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(139,92,246,0.08));
    border: 1px solid rgba(129,140,248,0.25);
    animation: processingAppear 0.35s ease;
}

.processing-spinner {
    width: 22px;
    height: 22px;
    flex: 0 0 22px;
    border: 3px solid rgba(255,255,255,0.16);
    border-top-color: #a5b4fc;
    border-right-color: #c084fc;
    border-radius: 50%;
    animation: processingSpin 0.8s linear infinite;
}

.processing-title {
    font-weight: 750;
    color: #f8fafc;
    font-size: 14px;
}

.processing-detail {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 3px;
}

@keyframes processingSpin {
    to { transform: rotate(360deg); }
}

@keyframes processingAppear {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}




"""

# ============================================================

# GRADIO UI

# ============================================================


# ============================================================
# GRADIO UI
# ============================================================

with gr.Blocks(
    title="Receipt Agent — Intelligent Order Assistant",
    css=custom_css,
    theme=gr.themes.Base(
        primary_hue="indigo",
        secondary_hue="purple",
        neutral_hue="slate"
    )
) as demo:

    # FULL-PAGE ANIMATED BACKGROUND
    gr.HTML(
        """
        <div class="space-background" aria-hidden="true">
            <span class="shooting-star"></span><span class="shooting-star"></span>
            <span class="shooting-star"></span><span class="shooting-star"></span>
            <span class="shooting-star"></span><span class="shooting-star"></span>
            <span class="shooting-star"></span><span class="shooting-star"></span>
            <span class="shooting-star"></span><span class="shooting-star"></span>
        </div>
        <div class="wave-background" aria-hidden="true">
            <div class="wave-line"></div>
        </div>
        """,
        elem_classes="background-layer",
        js_on_load="""
        (() => {
            const updateBackground = () => {
                const y = window.scrollY || document.documentElement.scrollTop || 0;
                document.body.classList.toggle('show-waves', y > Math.max(180, window.innerHeight * 0.35));
            };
            window.addEventListener('scroll', updateBackground, {passive: true});
            window.addEventListener('resize', updateBackground);
            setTimeout(updateBackground, 250);
            updateBackground();
        })();
        """
    )

    # HERO
    gr.HTML(
        """
        <div class="hero">
            <div class="hero-icon" aria-hidden="true">
                <svg viewBox="0 0 48 48">
                    <path d="M14 5h16l8 8v30H14z"/>
                    <path d="M30 5v10h8"/>
                    <path d="M20 23h12M20 29h12M20 35h8"/>
                </svg>
            </div>

            <div class="hero-title">
                Receipt Agent
            </div>

            <div class="hero-subtitle">
                Your intelligent receipt & order assistant.
                Upload a receipt, ask a question, and let the
                Agent handle order lookup, policy reasoning,
                return deadlines, and warranty information.
            </div>
        </div>
        """
    )

    # STATUS
    with gr.Row():

        gr.HTML(
            """
            <div class="status-card">
                <span style="color:#4ade80;">●</span>
                Agent Online
            </div>
            """
        )

        gr.HTML(
            """
            <div class="status-card">
                <span style="color:#a78bfa;">●</span>
                RAG Enabled
            </div>
            """
        )

        gr.HTML(
            """
            <div class="status-card">
                <span style="color:#60a5fa;">●</span>
                Tools Connected
            </div>
            """
        )

    gr.Markdown("")

    # MAIN AREA
    with gr.Row():

        # LEFT SIDE
        with gr.Column(scale=4):

            # UPLOAD
            with gr.Group(elem_classes=["panel", "upload-panel"]):

                gr.HTML(
                    """
                    <div class="section-title">
                        <span class="ui-icon"><svg viewBox="0 0 24 24"><path d="M12 16V4m0 0L7 9m5-5 5 5"/><path d="M5 14v5h14v-5"/></svg></span><span>Upload your receipt</span>
                    </div>

                    <div class="upload-intro">
                        <div class="upload-orb">
                            <svg viewBox="0 0 24 24"><path d="M12 15V4m0 0L8 8m4-4 4 4"/><path d="M5 13v5h14v-5"/></svg>
                        </div>
                        <div>
                            <div class="upload-copy-title">Drop your receipt into the workspace</div>
                            <div class="upload-copy-subtitle">PDF order confirmations are ready for analysis</div>
                        </div>
                    </div>
                    """
                )

                receipt_file = gr.File(
                    label="Receipt PDF",
                    file_types=[".pdf"],
                    type="filepath",
                    elem_classes="upload-box"
                )

                gr.HTML(
                    """
                    <div class="upload-hints">
                        <div class="upload-hint"><strong>PDF only</strong>Receipt format</div>
                        <div class="upload-hint"><strong>Auto-read</strong>Order details</div>
                        <div class="upload-hint"><strong>Agent ready</strong>Ask anything</div>
                    </div>
                    """
                )

            # QUESTION
            with gr.Group(elem_classes="panel"):

                gr.HTML(
                    """
                    <div class="section-title">
                        <span class="ui-icon"><svg viewBox="0 0 24 24"><path d="M4 5h16v11H8l-4 4z"/><path d="M8 9h8M8 12h5"/></svg></span><span>Ask your question</span>
                    </div>
                    """
                )

                question = gr.Textbox(
                    label="",
                    placeholder=(
                        "Example: When does my warranty expire?"
                    ),
                    lines=3
                )

                ask_button = gr.Button(
                    "Ask Receipt Agent",
                    elem_classes="ask-button",
                    variant="primary"
                )

                gr.HTML(
                    """
                    <div class="quick-title">
                        Quick questions
                    </div>
                    """
                )

                with gr.Row():

                    quick_return = gr.Button(
                        "Can I return this?",
                        elem_classes="quick-button"
                    )

                    quick_warranty = gr.Button(
                        "Warranty expiry?",
                        elem_classes="quick-button"
                    )

                with gr.Row():

                    quick_deadline = gr.Button(
                        "Return deadline?",
                        elem_classes="quick-button"
                    )

                    quick_order = gr.Button(
                        "Order details?",
                        elem_classes="quick-button"
                    )

        # RIGHT SIDE
        with gr.Column(scale=6):

            # RECEIPT INTELLIGENCE
            with gr.Group(elem_classes="panel"):

                gr.HTML(
                    """
                    <div class="section-title">
                        <span class="ui-icon"><svg viewBox="0 0 24 24"><path d="M7 3h10v18H7z"/><path d="M9 7h6M9 11h6M9 15h4"/></svg></span><span>Receipt intelligence</span>
                    </div>
                    """
                )

                status_output = gr.Markdown(
                    "Waiting for a receipt..."
                )

                receipt_output = gr.Markdown(
                    "Upload a receipt to see extracted information.",
                    elem_classes="receipt-box"
                )

                order_status = gr.Markdown(
                    ""
                )

            # AGENT ANSWER
            with gr.Group(elem_classes="panel"):

                gr.HTML(
                    """
                    <div class="section-title">
                        <span class="ui-icon"><svg viewBox="0 0 24 24"><rect x="4" y="6" width="16" height="13" rx="3"/><path d="M8 19v2l4-2 4 2v-2M9 11h.01M15 11h.01M9 15h6"/></svg></span><span>Agent Response</span>
                    </div>
                    """
                )

                answer_output = gr.Markdown(
                    """
                    ### Your assistant is ready

                    Upload a receipt and ask a question. I will combine the receipt details with the connected order data and policies to build your answer.

                    > Try asking about a return, warranty, deadline, or order details.

                    <div class="agent-status"><span class="agent-status-dot"></span>Waiting for your request</div>
                    """,
                    elem_classes="answer-box"
                )

    # FOOTER
    gr.HTML(
        """
        <div class="footer">

            <strong>Receipt Agent</strong>
            &nbsp;•&nbsp;
            Powered by LangChain + Groq + RAG + FAISS

            <br>

            Intelligent order assistance powered by your agent

        </div>
        """
    )

    # MAIN BUTTON
    ask_button.click(
        fn=process_receipt,
        inputs=[
            receipt_file,
            question
        ],
        outputs=[
            status_output,
            receipt_output,
            question,
            answer_output,
            order_status
        ]
    )

    # QUICK QUESTION BUTTONS
    quick_return.click(
        fn=lambda: "Can I return this product?",
        outputs=question
    )

    quick_warranty.click(
        fn=lambda: "When does my warranty expire?",
        outputs=question
    )

    quick_deadline.click(
        fn=lambda: "What is my return deadline?",
        outputs=question
    )

    quick_order.click(
        fn=lambda: "Show me my order details.",
        outputs=question
    )


# ============================================================
# LAUNCH
# ============================================================

if __name__ == "__main__":

    demo.launch()
