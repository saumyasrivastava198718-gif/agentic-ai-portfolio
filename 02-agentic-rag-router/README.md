# 🤖 Agentic RAG Router

A multi-source grounded AI assistant that intelligently routes user questions across:

- an indexed PDF knowledge base
- live web search
- or a hybrid of both

The system combines semantic routing, persistent vector retrieval, live web retrieval, grounded generation, source transparency, and graceful fallback behavior.

---

## 🎯 Problem

Traditional RAG applications often rely on one fixed source.

Real-world questions may require:

- internal document knowledge
- current web information
- both document and live information

This project introduces an intelligent routing layer that selects the appropriate retrieval path.

---

## 🏗️ Architecture

```mermaid
flowchart TD

A[User Question] --> B[Routing Layer]

B -->|PDF| C[PDF Retrieval]
B -->|Web| D[Web Retrieval]
B -->|Hybrid| E[PDF + Web Retrieval]

C --> F[Evidence]
D --> F
E --> F

F --> G[Grounded Answer Generator]

G --> H[Final Answer]
H --> I[Sources and Evidence]