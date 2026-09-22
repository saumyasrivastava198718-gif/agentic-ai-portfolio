# Applied Agentic AI & Generative AI Portfolio

A hands-on portfolio of AI engineering projects focused on:

- Retrieval-Augmented Generation (RAG)
- Vector Databases and Semantic Search
- Large Language Model Applications
- Agentic AI Systems
- Multi-Agent Workflows
- Model Context Protocol (MCP)
- Workflow Automation
- AI UX, Trust and Human-in-the-Loop Systems
- Python Data Analysis and AI Engineering

# 🤖 Agentic AI & GenAI Engineering Portfolio

A hands-on portfolio of AI, Generative AI, RAG, Agentic AI, multi-agent
systems, and Python projects developed while strengthening my practical
AI engineering and trainer-level understanding.

My focus is not only on using LLMs, but on understanding how production
AI systems are designed: retrieval, routing, planning, orchestration,
tool use, structured outputs, evaluation, reliability, observability,
guardrails, and human-in-the-loop workflows.

---

## 👩‍💻 About Me

I am an AI / GenAI practitioner and technical instructor with experience
teaching programming and AI concepts.

My current work focuses on:

- Generative AI
- Agentic AI
- Retrieval-Augmented Generation (RAG)
- Multi-Agent Systems
- Python
- LLM Application Development
- Vector Databases & Embeddings
- Agent Orchestration
- AI Evaluation & Reliability
- AI Automation

I use these projects to move from conceptual understanding to practical
implementation and to develop trainer-ready explanations of AI systems.

---

# 🚀 Featured Projects

## 1. PDF RAG Pipeline

An end-to-end Retrieval-Augmented Generation pipeline for querying
information from PDF documents.

### Implemented / Practiced

- PDF ingestion
- Text extraction with PyMuPDF
- Chunking with overlap
- Sentence Transformer embeddings
- Vector storage using ChromaDB
- Semantic similarity search
- Retrieval of relevant document chunks
- Metadata preservation
- Retrieval testing

### Architecture

PDF
→ Text Extraction
→ Chunking
→ Embeddings
→ Vector Database
→ Semantic Retrieval
→ Context
→ LLM
→ Answer

### Technologies

`Python` `PyMuPDF` `Sentence Transformers` `ChromaDB` `RAG`

### Engineering topics explored

- Chunk size and overlap
- Embedding dimensions
- Semantic vs keyword search
- Retrieval quality
- Hallucination reduction
- RAG evaluation
- Context grounding

---

## 2. Agentic RAG Router

A routing-based RAG architecture designed to decide how a query should
be processed before generating an answer.

### Concepts Practiced

- Query routing
- Agent decision logic
- Retrieval workflows
- Structured execution
- LLM-based decision making
- Fallback strategies
- Agentic RAG architecture

### Conceptual Flow

User Query
→ Router
→ Retrieval / Tool / LLM Path
→ Context
→ Response

---

## 3. Multi-Agent Workflow Planner

A modular multi-agent project exploring how complex objectives can be
decomposed into structured tasks and delegated across agents.

### Architecture

User Goal
→ Planner
→ Task Decomposition
→ Agent Assignment
→ Tool Execution
→ Result Aggregation
→ Final Response

### Project Structure

- `agents/`
- `planner/`
- `orchestration/`
- `models/`
- `tools/`
- `tests/`
- `app.py`

### Concepts Practiced

- Planning agents
- Task decomposition
- Agent roles
- Sequential execution
- Parallel execution
- State management
- Structured outputs
- Pydantic-style schemas
- Retry / fallback thinking
- Orchestration patterns

---

## 4. Production GTM Multi-Agent System

A production-oriented multi-agent architecture for Go-To-Market
research and strategy.

### Agent Roles

- Market Research Agent
- Customer Research Agent
- Competitor Analysis Agent
- GTM Strategy Agent

### Architecture

Business Objective
→ Orchestrator
→ Research Agents
→ Tools / External Data
→ Analysis
→ GTM Strategy
→ Final Output

### Engineering Concepts

- Multi-agent orchestration
- Specialized agent roles
- MCP concepts
- Tool integration
- Workflow coordination
- Monitoring
- Metrics
- Fallback handling
- Structured schemas

This project is being developed as a production-oriented exploration of
reliable multi-agent systems.

---

## 5. Agentic UX Trust Prototype

An exploration of Human-in-the-Loop design for AI systems where users
need visibility and control over important agent actions.

### Concepts

- Action previews
- Human approval
- User override
- Explainable agent actions
- Guardrails
- Trustworthy AI UX
- High-impact action confirmation

Example:

Agent proposes action
→ Show proposed action
→ Human reviews
→ Approve / Reject / Modify
→ Agent executes

---

## 6. AI Support Triage System

An agentic workflow for understanding and routing support requests.

### Concepts Practiced

- Request classification
- Routing
- Structured outputs
- Agent decisions
- Escalation
- Human-in-the-loop
- Error handling

---

# 🧠 Agentic AI Concepts Practiced

### Agent Fundamentals

- LLM + Tools + Memory + Planning
- ReAct pattern
- Tool calling
- Function calling
- Structured outputs
- Agent loops
- Task decomposition

### Multi-Agent Systems

- Supervisor / worker architecture
- Specialized agents
- Sequential workflows
- Parallel workflows
- Centralized orchestration
- Agent collaboration

### Reliability

- Retries
- Fallbacks
- Timeouts
- Error handling
- Maximum iteration limits
- Guardrails
- Human approval
- Validation

### Production Engineering

- Logging
- Monitoring
- Observability
- Tracing
- Evaluation
- Caching
- Cost optimization
- Latency optimization

---

# 🧩 Frameworks & Technologies Explored

## Agentic AI

`LangChain`
`LangGraph`
`CrewAI`
`AutoGen`
`Deep Agents`
`MCP`

## GenAI / LLM

`Gemini`
`Hugging Face`
`Transformers`
`Prompt Engineering`
`Structured Outputs`
`Function Calling`

## RAG

`PyMuPDF`
`Sentence Transformers`
`ChromaDB`
`Embeddings`
`Semantic Search`
`Vector Databases`

## Python

`Functions`
`Classes`
`Type Hints`
`Lists`
`Dictionaries`
`Exception Handling`
`Modules`
`OOP`
`Pydantic`
`TypedDict`

## Development

`VS Code`
`Git`
`GitHub`
`Virtual Environments`
`Streamlit`

---

# 🧪 Small Coding & Framework Exercises

Alongside the larger portfolio projects, I maintain smaller programs
for understanding individual concepts before integrating them into
larger AI systems.

Examples include:

- Python function exercises
- List and dictionary operations
- Type hints
- Exception handling
- Pydantic models
- TypedDict state definitions
- LangChain chains
- LangGraph StateGraph workflows
- START / END graph routing
- Single-agent workflows
- Multi-agent routing
- Tool calling
- Structured LLM outputs
- RAG retrieval functions
- Embedding generation
- Cosine similarity
- Semantic search
- Planner logic
- Agent routing logic

The goal is to understand both the individual building blocks and how
they combine into complete AI applications.

---

# 🏗️ How I Approach AI System Design

For each project I try to answer:

1. What problem are we solving?
2. Does this require an LLM?
3. Does it require RAG?
4. Does it require an agent?
5. When should execution be deterministic?
6. When should the LLM make a decision?
7. Should tasks execute sequentially or in parallel?
8. Where should state and memory be stored?
9. What happens when a tool fails?
10. How do we prevent infinite agent loops?
11. How do we evaluate the system?
12. Where should humans approve actions?
13. How do we protect sensitive information?
14. How do we reduce latency and cost?
15. How would the architecture scale to production?

---

# 🎯 Current Learning Focus

Currently strengthening:

- Agentic AI architecture
- LangGraph
- Multi-agent orchestration
- Production RAG
- MCP
- Agent evaluation
- AI observability
- RAG evaluation
- Tool reliability
- Human-in-the-loop systems
- Production deployment

---

# 📚 Learning Philosophy

I build projects at three levels:

### 1️⃣ Understand
Learn the concept and why it exists.

### 2️⃣ Implement
Write and debug the code myself.

### 3️⃣ Explain
Be able to explain the architecture, design choices, failure modes,
trade-offs, and production considerations.

This portfolio documents that progression from Python fundamentals to
production-oriented Agentic AI systems.

---

## 🚧 Portfolio Status

This repository is actively evolving.

Some projects are complete working prototypes, while others are
engineering explorations or works in progress as I continue developing
and testing more advanced Agentic AI architectures.

---

⭐ **Current focus:** Building reliable, explainable, and production-aware
Agentic AI systems while strengthening hands-on AI engineering skills.
# Saumya Srivastava
## AI | Generative AI | RAG | Agentic AI | Multi-Agent Systems

Hands-on AI engineering portfolio focused on building and understanding
RAG pipelines, vector search, LLM applications, Agentic AI systems,
multi-agent orchestration, MCP-based workflows, and production-aware
AI architectures.

This repository documents my progression from Python and AI foundations
to end-to-end GenAI and Agentic AI applications, with emphasis on
architecture, implementation, reliability, evaluation, and explainability.
