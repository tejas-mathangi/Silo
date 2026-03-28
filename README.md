# Silo 🏛️

**Current Status:** ✅ Phase 1 (Ingestion Pipeline & Dockerization Completed)

An enterprise-grade internal knowledge chatbot built with RAG (Retrieval-Augmented Generation). 
**Silo** enables users to query private organization documents (reports, policies, contracts, communications) using natural language while maintaining high standards for security, compliance, and monitoring.

---

## 🚀 Core Stack
- **Ingestion:** [Docling](https://github.com/DS4SD/docling) (parsing), [LangChain](https://www.langchain.com/) (chunking)
- **Embedding Model:** `nomic-ai/nomic-embed-text-v1.5` (768-dim)
- **Vector Database:** [Qdrant](https://qdrant.tech/) (with payload-based RBAC)
- **Containerization:** Docker + Docker Compose
- **Package Management:** [uv](https://github.com/astral-sh/uv)

---

## 🏛️ RBAC Access Matrix
The system enforces department-level and seniority-level scoping at the database level:

| Role | Level | Accessible Departments | Data Access |
| :--- | :--- | :--- | :--- |
| `c_suite` | L3 | ALL | Full access |
| `finance_manager` | L2 | finance | Reports, salaries, audits |
| `hr_manager` | L2 | hr | Payroll, records, pipeline |
| `operations` | L1 | operations | SOPs, vendor contracts |
| `employee` | L0 | global | Public policies only |

---

## 🛠️ Building and Running (Docker)

### 1. Start the Stack
This builds the app and starts both the Qdrant database and the Silo application.
```bash
docker compose up --build
```

### 2. Initialize & Seed Data
Prepare the database collection and ingest the initial sample documents (e.g., `finance_policy.md`).
```bash
# Initialize the collection
docker compose run --rm app python src/scripts/init_qdrant.py

# Seed sample data
docker compose run --rm app python src/scripts/seed_data.py
```

### 3. Test Retrieval
Verify that the ingestion worked by running a semantic search test.
```bash
docker compose run --rm app python src/scripts/test_retrieval.py
```

---

## 📂 Project Structure (Phase 1)
- `src/core/config.py`: Centralized Pydantic settings and environment management.
- `src/ingestion/parser.py`: Document parsing using Docling.
- `src/ingestion/chunker.py`: Smart text splitting with LangChain.
- `src/ingestion/metadata.py`: RBAC-compliant metadata schemas.
- `src/ingestion/embedder.py`: Vector generation using Nomic AI.
- `src/database/qdrant.py`: Qdrant collection and indexing management.
- `src/ingestion/pipeline.py`: Orchestrates the full ingestion flow.

---

## 📝 Development Conventions
- **Hot-Reloading:** The `app` service uses Docker Volumes. Changes to `src/` are reflected instantly inside the container.
- **Dependencies:** Managed via `pyproject.toml`. Run `docker compose up --build` if you add new libraries.
- **Logging:** All major architectural changes must be documented in `DEVELOPMENT_LOG.md`.
- **Security:** Never commit your `.env` file (already in `.gitignore`).

---

## 🗺️ Roadmap
1. ✅ **Phase 1:** Ingestion Pipeline & Dockerization
2. 🕒 **Phase 2:** Basic RAG Chain (LLM Integration)
3. 🕒 **Phase 3:** Auth + RBAC Enforcement
4. 🕒 **Phase 4:** Guardrails & PII Redaction
5. 🕒 **Phase 5:** Summarization & Reports
6. 🕒 **Phase 6:** Monitoring & Evaluation (LangSmith)
7. 🕒 **Phase 7:** Streamlit Frontend
8. 🕒 **Phase 8:** Azure Deployment & CI/CD
