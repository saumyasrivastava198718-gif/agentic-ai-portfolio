# 🛡️ Agentic UX Trust Prototype

A production-inspired **Agentic AI decision-support prototype** demonstrating how AI systems can provide transparent recommendations while preserving **human control, safety, traceability, and trust**.

The project uses a financial decision-support scenario to demonstrate an important Agentic AI principle:

> AI may analyze, retrieve evidence, reason, and propose actions — but high-impact financial actions must remain under explicit human control.

This is an **educational prototype only**. It does not execute real financial transactions and does not provide personalized financial advice.

---

## 🎯 Project Objective

Many AI demos focus only on generating an answer.

Real-world Agentic AI systems also need mechanisms for:

- deterministic safety controls
- transparent action previews
- evidence-grounded reasoning
- structured outputs
- human approval
- overrides and cancellation
- evaluation
- telemetry and observability
- testing
- failure handling

This project demonstrates these concepts through a small but professionally structured Agentic AI application.

---

## 🏗️ High-Level Architecture

```text
User
  │
  ▼
Streamlit UI
  │
  ▼
Pydantic / Structured Request
  │
  ▼
Deterministic Safety Guardrail
  │
  ├── Unsafe request ──► BLOCK
  │
  └── Safe request
          │
          ▼
     Trust Workflow
          │
          ▼
   Evidence Retrieval
          │
          ▼
     Agent Proposal
          │
          ├── Summary
          ├── Reasoning Summary
          ├── Evidence / Citations
          ├── Assumptions
          ├── Risks
          ├── Proposed Actions
          └── Confidence Indicator
          │
          ▼
   Trust & Safety Evaluation
          │
          ▼
       Telemetry
          │
          ▼
   Human-in-the-Loop
      /      |      \
 Approve  Override  Cancel
```

---

## ✨ Core Features

### 1. Deterministic Safety Guardrails

High-risk transaction requests are checked before the agent workflow begins.

Examples include requests to:

- execute trades
- place orders
- automatically buy or sell
- transfer money
- send money

Such requests are blocked before proposal generation.

Example:

```text
Request blocked:
This prototype provides decision support only
and does not execute financial transactions.
```

This demonstrates an important production pattern:

```text
Deterministic policy enforcement
        BEFORE
probabilistic LLM reasoning
```

---

### 2. Evidence-Grounded Agent Proposals

For permitted decision-support questions, the workflow retrieves relevant evidence and generates a structured proposal.

The proposal can contain:

- summary
- reasoning summary
- supporting evidence
- source identifiers
- retrieval relevance indicators
- assumptions
- risks
- proposed actions
- confidence indicator

This improves transparency compared with an opaque AI response.

---

### 3. Action Preview

The system displays proposed actions before any human decision.

The user can inspect:

- what the AI proposes
- why it proposes it
- what evidence supports it
- assumptions
- risks
- confidence information

This implements the **preview-before-action** UX pattern for trustworthy agents.

---

### 4. Human-in-the-Loop Control

Material actions require explicit human review.

The reviewer can:

```text
Approve
Override
Cancel
```

#### Approve

Accepts the proposal while still executing no real financial transaction.

#### Override

Allows the human reviewer to modify the proposed course of action.

#### Cancel

Stops the action completely.

This demonstrates bounded autonomy rather than unrestricted agent autonomy.

---

### 5. Trust & Safety Evaluation

Generated proposals are evaluated before being presented as trusted output.

The evaluation layer provides an additional safety and quality checkpoint around agent behavior.

---

### 6. Telemetry and Observability

The application exposes run telemetry to help inspect workflow behavior.

Production Agentic AI systems require observability because developers need to understand:

- what happened
- which component made a decision
- what evidence was retrieved
- whether safeguards activated
- where failures occurred
- how the workflow behaved

---

### 7. Confidence Indicator

The interface displays an application-level confidence indicator.

It is explicitly described as:

> An application confidence indicator, not a calibrated probability or guarantee of correctness.

This distinction prevents a UI confidence value from being misrepresented as statistical certainty.

---

## 🔐 Guardrail + HITL Defense-in-Depth

The project intentionally contains more than one safety mechanism.

```text
Layer 1
Input validation

Layer 2
Deterministic safety guardrail

Layer 3
Evidence-grounded proposal generation

Layer 4
Trust & safety evaluation

Layer 5
Human approval / override / cancellation

Layer 6
Telemetry and testing
```

These mechanisms serve different purposes.

A **guardrail** prevents prohibited requests from entering the agent workflow.

**Human-in-the-loop approval** controls permitted but consequential proposals.

Using both demonstrates **defense in depth**.

---

## 🧪 Testing

The project includes automated tests for major safety and workflow behaviors.

Current test coverage includes:

```text
test_transaction_request_blocked
test_retriever_returns_evidence
test_valid_request
test_short_question_rejected
test_proposal_requires_approval
test_cancel_stops_action
test_override_changes_action
test_evaluation_passes_safe_proposal
```

Run the complete test suite with:

```bash
python -m pytest -v
```

Current verified result:

```text
8 passed
```

---

## 🐛 Important Integration Lesson

During development, the deterministic guardrail passed its isolated unit test, but an end-to-end Streamlit test revealed that the guardrail was not initially invoked before proposal generation.

The application flow was corrected from:

```text
Request
   ↓
Agent Proposal
   ↓
Human Approval
```

to:

```text
Request
   ↓
Deterministic Guardrail
   ↓
Blocked OR Continue
              ↓
        Agent Proposal
              ↓
        Human Approval
```

This demonstrates an important software-engineering lesson:

> Passing unit tests does not guarantee that components are correctly integrated.

Both **unit testing and end-to-end/integration testing** are necessary for reliable Agentic AI systems.

---

## 📂 Project Structure

```text
05-agentic-ux-trust/
│
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── src/
│   ├── agent/
│   ├── evaluation/
│   ├── guardrails/
│   │   └── safety.py
│   ├── models/
│   └── workflow/
│
└── tests/
    ├── test_guardrails.py
    ├── test_retrieval.py
    ├── test_schemas.py
    └── test_workflow.py
```

---

## 🚀 Running the Application

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate it on Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run tests

```bash
python -m pytest -v
```

### 5. Start the Streamlit application

```bash
python -m streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

---

## 🛡️ Example Safety Test

### Financial Question

```text
Please execute trade automatically using this portfolio.
```

### Scenario

```text
I have ₹5,00,000 and want the AI to purchase technology stocks.
```

Expected result:

```text
Request blocked:
This prototype provides decision support only
and does not execute financial transactions.
```

The request should not reach normal Agent Proposal generation.

---

## 🧠 Engineering Concepts Demonstrated

This project demonstrates:

- Agentic AI UX
- trustworthy AI design
- human-in-the-loop systems
- deterministic guardrails
- bounded autonomy
- structured outputs
- Pydantic validation
- evidence retrieval
- transparent reasoning summaries
- action previews
- risk communication
- confidence communication
- evaluation
- telemetry
- observability
- workflow state
- approval gates
- override mechanisms
- cancellation
- unit testing
- integration testing
- defense-in-depth safety

---

## 💡 Why This Architecture?

An LLM is probabilistic.

A rule such as:

```text
Never execute a real financial transaction
without authorization.
```

should therefore not depend entirely on the model deciding whether to obey it.

Deterministic application logic can enforce hard boundaries, while the AI component handles tasks where language understanding and reasoning are useful.

This separation creates a safer architecture:

```text
Code controls permissions.
AI assists with reasoning.
Humans retain authority.
```

---

## 🏭 Production Extensions

A production implementation could extend this prototype with:

- authenticated users
- role-based access control
- persistent audit logs
- durable workflow state
- policy engines
- model/provider fallbacks
- retry policies with backoff
- timeout handling
- caching
- calibrated uncertainty
- adversarial safety testing
- prompt-injection defenses
- stronger retrieval evaluation
- automated Agent/LLM evaluations
- tracing platforms
- production monitoring
- latency and cost tracking
- encrypted storage
- secret management
- approval escalation policies

For financial applications, additional regulatory, security, privacy, compliance, and governance controls would also be required.

---

## ⚠️ Disclaimer

This repository is an educational Agentic AI prototype.

It does **not**:

- execute trades
- transfer money
- connect to brokerage accounts
- provide personalized investment advice
- guarantee the correctness of AI-generated information

All financial scenarios are hypothetical and used only to demonstrate AI engineering and trustworthy agent design.

---

## 📌 Portfolio Takeaway

The project demonstrates that building an Agentic AI system is not simply about giving an LLM tools.

A trustworthy agent needs:

```text
Reasoning
+ Evidence
+ Deterministic Boundaries
+ Human Control
+ Evaluation
+ Observability
+ Testing
```

The goal is not maximum autonomy.

The goal is **useful autonomy within explicit, testable and observable boundaries**.