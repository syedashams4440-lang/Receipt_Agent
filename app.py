import gradio as gr

from receipt_parser import extract_receipt
from agent import ask_agent


# ============================================================
# PROCESS RECEIPT
# ============================================================

def process_receipt(pdf_file, question):

    if pdf_file is None:
        return (
            "⚠️ Please upload a receipt PDF.",
            "",
            "",
            "",
            ""
        )

    if not question or not question.strip():
        return (
            "⚠️ Please enter a question.",
            "",
            "",
            "",
            ""
        )

    try:
        # Extract receipt information
        receipt = extract_receipt(pdf_file)

        order_id = receipt["order_id"]
        product = receipt["product"]
        purchase_date = receipt["purchase_date"]

        if not order_id:
            return (
                "❌ I couldn't find an Order ID in this receipt.",
                "",
                "",
                "",
                ""
            )

        # ----------------------------------------------------
        # Build receipt information
        # ----------------------------------------------------

        receipt_info = f"""
### 🧾 Receipt Details

**Order ID**  
`{order_id}`

**Product**  
{product}

**Purchase Date**  
{purchase_date}
"""

        # ----------------------------------------------------
        # Send request to agent
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

        response = ask_agent(agent_question)

        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return (
            "🟢 Receipt processed successfully",
            receipt_info,
            question,
            response.content,
            f"Order `{order_id}`"
        )

    except Exception as e:

        print("\n========== APPLICATION ERROR ==========")
        print(e)
        print("=======================================\n")

        return (
            "🔴 Something went wrong while processing the receipt.",
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
   GLOBAL
========================================================= */

body {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(99, 102, 241, 0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(168, 85, 247, 0.16),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #080b16 0%,
            #101426 45%,
            #080b16 100%
        );

    color: #f8fafc;
}


/* =========================================================
   MAIN CONTAINER
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
            rgba(15, 23, 42, 0.88)
        );

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 25px 70px rgba(0,0,0,0.45);

    text-align: center;
}


.hero-icon {
    font-size: 54px;
    margin-bottom: 10px;
}


.hero-title {
    font-size: 42px;
    font-weight: 800;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #a5b4fc,
            #c084fc
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 10px;
}


.hero-subtitle {
    color: #94a3b8;
    font-size: 17px;
    max-width: 700px;
    margin: auto;
    line-height: 1.7;
}


/* =========================================================
   STATUS
========================================================= */

.status-card {

    padding: 14px 18px;

    border-radius: 14px;

    background:
        rgba(34, 197, 94, 0.08);

    border:
        1px solid rgba(34, 197, 94, 0.25);

    color: #86efac;

    font-weight: 600;

    text-align: center;
}


/* =========================================================
   PANELS
========================================================= */

.panel {

    background:
        rgba(15, 23, 42, 0.78);

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius: 20px;

    padding: 22px;

    box-shadow:
        0 15px 45px rgba(0,0,0,0.25);

    backdrop-filter: blur(15px);
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
        1px dashed rgba(129, 140, 248, 0.55);

    border-radius: 18px;

    background:
        rgba(99, 102, 241, 0.05);

    padding: 12px;

    transition: 0.25s ease;
}


.upload-box:hover {

    border-color:
        rgba(167, 139, 250, 0.9);

    background:
        rgba(99, 102, 241, 0.10);

}


/* =========================================================
   INPUT
========================================================= */

textarea,
input {

    border-radius: 12px !important;

    border:
        1px solid rgba(255,255,255,0.10) !important;

    background:
        rgba(15,23,42,0.85) !important;

    color: #f8fafc !important;
}


/* =========================================================
   ASK BUTTON
========================================================= */

.ask-button {

    border-radius: 14px !important;

    border: none !important;

    background:
        linear-gradient(
            135deg,
            #6366f1,
            #8b5cf6
        ) !important;

    color: white !important;

    font-size: 16px !important;

    font-weight: 700 !important;

    padding: 15px !important;

    box-shadow:
        0 10px 30px rgba(99,102,241,0.35);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}


.ask-button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 15px 40px rgba(139,92,246,0.45);
}


/* =========================================================
   ANSWER
========================================================= */

.answer-box {

    border-radius: 18px !important;

    background:
        linear-gradient(
            135deg,
            rgba(30,41,59,0.90),
            rgba(15,23,42,0.90)
        ) !important;

    border:
        1px solid rgba(129,140,248,0.20) !important;

}


/* =========================================================
   RECEIPT INFO
========================================================= */

.receipt-box {

    border-radius: 16px;

    background:
        rgba(30,41,59,0.65);

    border:
        1px solid rgba(255,255,255,0.07);

    padding: 18px;

}


/* =========================================================
   QUICK QUESTIONS
========================================================= */

.quick-title {

    color: #94a3b8;

    font-size: 13px;

    font-weight: 600;

    margin-top: 8px;
}


.quick-button {

    border-radius: 12px !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;

    background:
        rgba(30,41,59,0.65) !important;

    color: #cbd5e1 !important;

    transition: 0.2s ease;
}


.quick-button:hover {

    background:
        rgba(99,102,241,0.18) !important;

    border-color:
        rgba(129,140,248,0.4) !important;

}


/* =========================================================
   FOOTER
========================================================= */

.footer {

    text-align: center;

    margin-top: 25px;

    padding: 20px;

    color: #64748b;

    font-size: 13px;
}


/* =========================================================
   HIDE GRADIO FOOTER
========================================================= */

footer {
    display: none !important;
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 700px) {

    .hero-title {
        font-size: 30px;
    }

    .hero {
        padding: 30px 20px;
    }

    .gradio-container {
        padding: 12px !important;
    }
}

"""


# ============================================================
# GRADIO UI
# ============================================================

with gr.Blocks(
    title="ReceiptAI — Intelligent Order Assistant",
    css=custom_css,
    theme=gr.themes.Base(
        primary_hue="indigo",
        secondary_hue="purple",
        neutral_hue="slate"
    )
) as demo:

    # ========================================================
    # HERO
    # ========================================================

    gr.HTML(
        """
        <div class="hero">

            <div class="hero-icon">
                🧾
            </div>

            <div class="hero-title">
                ReceiptAI
            </div>

            <div class="hero-subtitle">
                Your intelligent receipt & order assistant.
                Upload a receipt, ask a question, and let the
                AI handle order lookup, policy reasoning,
                return deadlines, and warranty information.
            </div>

        </div>
        """
    )

    # ========================================================
    # STATUS
    # ========================================================

    with gr.Row():

        gr.HTML(
            """
            <div class="status-card">
                🟢 AI Agent Online
            </div>
            """
        )

        gr.HTML(
            """
            <div class="status-card">
                🧠 RAG Enabled
            </div>
            """
        )

        gr.HTML(
            """
            <div class="status-card">
                🔧 Tools Connected
            </div>
            """
        )

    gr.Markdown("")

    # ========================================================
    # MAIN AREA
    # ========================================================

    with gr.Row():

        # ----------------------------------------------------
        # LEFT SIDE
        # ----------------------------------------------------

        with gr.Column(scale=4):

            with gr.Group(elem_classes="panel"):

                gr.HTML(
                    """
                    <div class="section-title">
                        📤 Upload your receipt
                    </div>

                    <div style="
                        color:#94a3b8;
                        margin-bottom:15px;
                        font-size:14px;
                    ">
                        Upload a PDF receipt or order confirmation.
                    </div>
                    """
                )

                receipt_file = gr.File(
                    label="Receipt PDF",
                    file_types=[".pdf"],
                    type="filepath",
                    elem_classes="upload-box"
                )

                gr.Markdown(
                    """
                    **Supported:** PDF receipts

                    Your receipt is analyzed to identify
                    the Order ID, product and purchase date.
                    """
                )

            # ------------------------------------------------
            # QUESTION
            # ------------------------------------------------

            with gr.Group(elem_classes="panel"):

                gr.HTML(
                    """
                    <div class="section-title">
                        💬 Ask your question
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
                    "✨ Ask ReceiptAI",
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
                        "↩️ Can I return this?",
                        elem_classes="quick-button"
                    )

                    quick_warranty = gr.Button(
                        "🛡️ Warranty expiry?",
                        elem_classes="quick-button"
                    )

                with gr.Row():

                    quick_deadline = gr.Button(
                        "📅 Return deadline?",
                        elem_classes="quick-button"
                    )

                    quick_order = gr.Button(
                        "📦 Order details?",
                        elem_classes="quick-button"
                    )

        # ----------------------------------------------------
        # RIGHT SIDE
        # ----------------------------------------------------

        with gr.Column(scale=6):

            with gr.Group(elem_classes="panel"):

                gr.HTML(
                    """
                    <div class="section-title">
                        📋 Receipt intelligence
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

            # ------------------------------------------------
            # AI ANSWER
            # ------------------------------------------------

            with gr.Group(elem_classes="panel"):

                gr.HTML(
                    """
                    <div class="section-title">
                        🤖 AI Agent Response
                    </div>
                    """
                )

                answer_output = gr.Markdown(
                    """
                    ### 👋 Hello!

                    Upload a receipt and ask me something like:

                    > **"Can I return this product?"**

                    or

                    > **"When does my warranty expire?"**
                    """,
                    elem_classes="answer-box"
                )

    # ========================================================
    # FOOTER
    # ========================================================

    gr.HTML(
        """
        <div class="footer">

            <strong>ReceiptAI</strong>
            &nbsp;•&nbsp;
            Powered by LangChain + Groq + RAG + FAISS

            <br>

            Intelligent order assistance powered by AI

        </div>
        """
    )

    # ========================================================
    # MAIN BUTTON
    # ========================================================

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

    # ========================================================
    # QUICK QUESTION BUTTONS
    # ========================================================

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