# 🧾 Receipt & Order Assistant

An AI-powered receipt and order assistant built for the Track 5 hackathon problem statement.

The application allows users to upload a receipt PDF and ask questions about their order, return eligibility, return deadlines, and warranty deadlines.

## 🚀 Features

- Upload receipt PDF
- Extract Order ID, product, and purchase date
- Look up orders from a mock database
- Search return and warranty policies using RAG
- Calculate return deadlines
- Calculate warranty deadlines
- Warn users when fewer than 7 days remain for a return
- Handle unknown Order IDs without hallucinating information
- Tool calling with a ReAct-style agent
- Gradio web interface

## 🧠 AI Architecture

The project follows the core agent pipeline taught in the workshop:

1. LLM setup
2. Document loading
3. Text splitting
4. Embeddings
5. FAISS vector store
6. Retriever
7. RAG
8. Custom tools
9. Tool calling
10. ReAct-style agent
11. Gradio deployment

## 🏗️ Architecture

```text
User
 │
 ▼
Gradio UI
 │
 ▼
Receipt PDF
 │
 ▼
Receipt Parser
 │
 ▼
Order ID
 │
 ▼
ReAct-style Agent
 │
 ├───────────────┬────────────────┐
 ▼               ▼                ▼
Order Tool    Policy Tool    Deadline Tools
 │               │                │
 ▼               ▼                ▼
Mock DB       FAISS + RAG     Date Calculation
                 │
                 ▼
          Store Policy Documents