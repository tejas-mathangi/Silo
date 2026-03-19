# Silo 🏛️

An enterprise-grade internal knowledge chatbot built with RAG (Retrieval-Augmented Generation).
Query your organization's private documents — reports, policies, contracts, and communications — using natural language.

## What it does
- Answers questions, summarizes documents, and generates reports from private company data
- Enforces Role-Based Access Control (RBAC) at the vector database layer — not just the UI
- Blocks PII leakage, out-of-scope queries, and prompt injection via a multi-stage guardrails pipeline
- Monitors every query for latency, token cost, and response quality via LangSmith
- Runs automated RAGAS evaluations on every deployment through CI/CD

## Access Model
Each user's retrieval is scoped by department and seniority level — enforced directly via Qdrant payload filters.
Finance sees finance. HR sees HR. Nothing leaks across.