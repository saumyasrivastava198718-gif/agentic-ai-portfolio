# Multi-Agent Workflow Planner

A stateful multi-agent startup accelerator built with Python,
LangGraph, Gemini, DDGS web search, Pydantic, and Streamlit.

## Overview

The application accepts a startup goal and coordinates specialized
agents to research, analyze, strategize, write, and review a final
startup deliverable.

## Architecture

User Goal
   ↓
Planner
   ↓
Researcher + Web Search
   ↓
Analyst
   ↓
Strategist
   ↓
Writer
   ↓
Reviewer
   ├── Approve → END
   └── Revise → Writer

LangGraph manages shared workflow state, node execution,
conditional routing, and a bounded revision cycle.

## Agents

### Planner
Breaks the user goal into specialized tasks.

### Researcher
Retrieves current web evidence using DDGS and uses an LLM for
synthesis when available.

### Analyst
Analyzes research evidence and extracts customer, opportunity,
competitive, technology, and risk signals.

### Strategist
Transforms analysis into an actionable startup strategy.

### Writer
Creates the final professional deliverable.

### Reviewer
Evaluates the draft and either approves it or requests revision.

## Reliability

The application supports graceful degradation.

When Gemini is available, agents can use LLM reasoning and
generation.

When Gemini is unavailable or quota-limited, deterministic Python
fallbacks allow the workflow to continue without fabricating
unsupported market information.

The Researcher uses independent web retrieval so retrieved evidence
can survive an LLM outage.

## Technologies

- Python
- LangGraph
- Google Gemini API
- Pydantic
- DDGS
- Streamlit
- python-dotenv

## Key Concepts Demonstrated

- Multi-agent architecture
- Stateful orchestration
- Shared workflow state
- Agent specialization
- Tool use
- Web retrieval
- LLM integration
- Deterministic fallbacks
- Conditional routing
- Revision loops
- Structured validation
- Graceful degradation

## Run Locally

Create and activate a virtual environment.

Install dependencies:

```bash
pip install -r requirements.txt