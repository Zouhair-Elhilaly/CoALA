# Project Handoff: Building a CoALA Research Agent

## 1. Project Identity

**Project Name:** CoALA Research Agent

**Research Foundation:** Cognitive Architectures for Language Agents (CoALA): A Conceptual Framework.

**Paper:** Cognitive Architectures for Language Agents (2024), published in Transactions on Machine Learning Research.

**Primary Objective:**

Build a powerful, modular, locally running AI Research Agent based on the CoALA cognitive architecture.

This is both:
1. A serious software engineering project.
2. A practical learning project to deeply understand and implement cognitive architectures for language agents.

I do not want a simple chatbot or a basic tool-calling agent.

I want to understand how the agent manages its memories, reasons, retrieves knowledge, learns from experience, selects actions, and interacts with its environment.

The project should be developed incrementally, with practical experiments and tests for every component.

---

## 2. My Current Environment

### Operating System
- Windows.
- PowerShell.
- VS Code.
- Main project drive: E:.

### Hardware
- Intel CPU.
- 8 GB RAM.
- 256 GB SSD.
- No dedicated NVIDIA GPU.
- Limited local computational resources.

### LLM
- Qwen 1.5B.
- Already installed locally through Ollama.
- Ollama is working.
- Model name must be verified using `ollama list` before implementation.

### Database
- Oracle AI Database 26ai Free.
- Oracle Database service: `FREEPDB1`.
- Database name: `FREE`.
- PDB status: READ WRITE.
- SQL*Plus version: 23.26.3.0.0.
- SQL Developer / SQL*Plus available.

Oracle connection verified:

`sqlplus system@localhost:1521/FREEPDB1`

Current administrative connection:
- Container: FREEPDB1
- User: SYSTEM

Previous SQL*Plus connection as SCOTT showed:
- DB_NAME: FREE
- SERVICE_NAME: SYS$USERS
- CURRENT_SCHEMA: SCOTT

Important: Use FREEPDB1 for the application connection, not SYS$USERS.

### Dedicated Application User

The next database setup task is to create a dedicated user:

`COALA_USER`

It has NOT yet been confirmed that this user was created.

Suggested initial setup, executed as SYSTEM inside FREEPDB1:

```sql
CREATE USER COALA_USER
IDENTIFIED BY "YOUR_STRONG_PASSWORD";

GRANT CREATE SESSION,
      CREATE TABLE,
      CREATE SEQUENCE,
      CREATE VIEW
TO COALA_USER;

ALTER USER COALA_USER QUOTA 100M ON USERS;
```

Never put database passwords directly in source code or commit them to Git.

---

## 3. Architecture: CoALA

The implementation must follow the concepts presented in the original CoALA paper.

### A. Memory System

Four memory types:

**1. Working Memory**
- Current task.
- Current observations.
- Active goals.
- Retrieved knowledge.
- Intermediate reasoning results.
- Candidate actions.
- Current agent state.

Implementation:
- Python data structures / Pydantic models.
- Primarily held in RAM.
- Optional persistent snapshots in Oracle.

**2. Episodic Memory**
- Previous agent experiences.
- Conversations.
- Actions executed.
- Observations.
- Successes and failures.
- Experiment histories.

Implementation:
- Oracle tables.
- Timestamped episodes.
- Relationships between sessions and episodes.

**3. Semantic Memory**
- General knowledge about the world.
- Facts extracted from research papers.
- Scientific concepts.
- Relationships between concepts.
- Retrieved document passages.

Implementation:
- Oracle relational tables.
- Document storage metadata.
- Document chunks.
- Later, Oracle 26ai VECTOR columns and vector search.

**4. Procedural Memory**
Two forms:
- Implicit knowledge stored in model weights.
- Explicit knowledge implemented in source code.

Implementation:
- Qwen model weights through Ollama.
- Python procedures and skills.
- Versioned skill metadata in Oracle.

Do not confuse skill metadata with executable Python code.

### B. Action Space

CoALA defines four action types.

**Internal Actions:**

1. Retrieval:
   - Read information from long-term memory.
   - Retrieve previous experiences.
   - Retrieve semantic knowledge.

2. Reasoning:
   - Use the LLM to process information.
   - Update working memory.
   - Generate plans and candidate actions.

3. Learning:
   - Write new experiences to episodic memory.
   - Add new knowledge to semantic memory.
   - Improve future behavior through experience.

**External Actions:**

4. Grounding:
   - Execute tools.
   - Read PDF files.
   - Perform calculations.
   - Search documents.
   - Interact with external environments.

Important distinction:
Reasoning, Retrieval and Learning are internal actions. Grounding interacts with external environments.

### C. Decision Making

Implement a repeated decision cycle:

1. Observation.
2. Proposal.
3. Evaluation.
4. Selection.
5. Execution.
6. New observation.
7. Update memory.
8. Repeat when necessary.

The controller must not blindly execute every LLM proposal.

Requirements:
- Validate proposed actions.
- Check available tools.
- Apply action permissions.
- Handle failures.
- Prevent infinite loops.
- Keep execution traces.
- Allow rejection of unsafe or invalid proposals.

The agent should support multiple actions and iterative planning, not just a single LLM response.

---

## 4. Technology Stack

Use this stack:

| Component | Technology |
|---|---|
| Main language | Python |
| Local LLM | Qwen 1.5B |
| Model runtime | Ollama |
| LLM communication | Ollama HTTP API |
| Database | Oracle AI Database 26ai |
| Oracle driver | python-oracledb |
| Data validation | Pydantic |
| Testing | Pytest |
| Document processing | PyMuPDF |
| Embeddings | A suitable lightweight embedding model, selected later |
| Vector storage | Oracle 26ai VECTOR |
| API | FastAPI, later |
| Agent orchestration | Custom Python controller initially |
| Optional orchestration | LangGraph, after understanding the custom implementation |
| Version control | Git / GitHub |

Do not introduce unnecessary frameworks during Phase 1.

Ollama currently runs Qwen. Do not migrate the model to PyTorch or download another model without a clear technical reason.

PyTorch can be introduced later for experiments involving neural networks, learning policies, and model training.

---

## 5. Project Structure

Target structure:

```text
CoALA_Research_Agent/
│
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── state.py
│   ├── decision.py
│   └── controller.py
│
├── memory/
│   ├── __init__.py
│   ├── working.py
│   ├── episodic.py
│   ├── semantic.py
│   └── procedural.py
│
├── actions/
│   ├── __init__.py
│   ├── reasoning.py
│   ├── retrieval.py
│   ├── learning.py
│   └── grounding.py
│
├── llm/
│   ├── __init__.py
│   ├── base.py
│   └── ollama_client.py
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── schema.sql
│   └── repositories/
│       ├── sessions.py
│       ├── episodes.py
│       ├── knowledge.py
│       └── documents.py
│
├── tools/
│   ├── __init__.py
│   ├── pdf_reader.py
│   ├── calculator.py
│   └── document_search.py
│
├── research/
│   ├── __init__.py
│   ├── chunking.py
│   ├── embeddings.py
│   └── retrieval.py
│
├── tests/
│   ├── test_memory.py
│   ├── test_actions.py
│   ├── test_decision.py
│   ├── test_database.py
│   └── test_llm.py
│
└── logs/
```

Adapt the structure when justified. Do not create empty files for every module at the beginning.

---

## 6. Database Design

Use Oracle 26ai as the persistent storage system.

Initial candidate tables:

- AGENT_SESSIONS
- DOCUMENTS
- DOCUMENT_CHUNKS
- KNOWLEDGE_ITEMS
- EPISODES
- ACTION_LOG
- SKILL_METADATA

Important design requirements:

- Primary keys.
- Foreign keys.
- Appropriate indexes.
- Created and updated timestamps.
- Session relationships.
- Document provenance.
- Action status and execution results.
- JSON columns only where flexible structured data is useful.

Working memory primarily lives in Python, not Oracle.

Procedural memory's executable code lives in Python and the model weights. Oracle stores skill metadata and version information.

Do not implement Vector Search immediately. First make relational storage and retrieval work correctly.

Later, introduce:
- Embedding generation.
- VECTOR columns.
- Similarity search.
- Semantic retrieval.
- Hybrid retrieval (keyword + vector).

---

## 7. Development Roadmap

### Phase 0 — Environment Validation

Current status:

- [x] Ollama works.
- [x] Qwen is installed locally (exact tag still needs verification).
- [x] Oracle 26ai is installed.
- [x] FREEPDB1 is open READ WRITE.
- [x] SYSTEM can connect to FREEPDB1.
- [ ] Confirm COALA_USER creation.
- [ ] Verify Ollama model tag.
- [ ] Create Python virtual environment.
- [ ] Install initial dependencies.
- [ ] Verify Python-to-Oracle connectivity.
- [ ] Verify Python-to-Ollama connectivity.

### Phase 1 — CoALA Core

Build:
- WorkingMemory.
- AgentState.
- Action definitions.
- Action registry.
- Decision controller.
- Proposal / Evaluation / Selection.
- Action execution.
- Observation handling.

Initially use simple deterministic mock actions so we can understand the architecture before adding the LLM.

### Phase 2 — Oracle Memory

Implement:
- Database connection management.
- SQL schema.
- Repository pattern.
- Episodic memory persistence.
- Semantic knowledge storage.
- Session persistence.
- Integration tests.

### Phase 3 — Qwen Integration

Connect the local Qwen model through Ollama.

Implement:
- LLM client abstraction.
- Prompt construction.
- Structured JSON outputs.
- Action proposal generation.
- Output validation.
- Retry and failure handling.

The LLM proposes actions; Python validates and executes them.

### Phase 4 — Research Agent Capabilities

Implement:
- PDF ingestion.
- Text extraction.
- Chunking.
- Document metadata.
- Embedding generation.
- Oracle Vector Search.
- Retrieval-Augmented Generation.
- Source-aware answers.

### Phase 5 — Learning and Reflection

Implement:
- Experience recording.
- Episodic retrieval.
- Reflection.
- Semantic knowledge extraction.
- Controlled knowledge updates.
- Experience-based improvements.

Do not allow autonomous modifications to executable Python code.

### Phase 6 — Advanced Decision Making

Implement:
- Multiple candidate actions.
- Action evaluation.
- Iterative planning.
- Bounded retries.
- Alternative strategies.
- Conflicting evidence handling.
- Explicit uncertainty.

### Phase 7 — Evaluation

Build an evaluation suite.

Measure:
- Retrieval precision and recall.
- Answer faithfulness to sources.
- Action selection accuracy.
- Tool execution success rate.
- Memory persistence.
- Decision cycle length.
- Latency and resource usage.
- Failure recovery.

Create repeatable benchmark tasks.

### Phase 8 — Deployment

Only after the core works:
- FastAPI.
- Web interface.
- Session management.
- Logging.
- Documentation.
- GitHub release.
- Demonstration examples.

---

## 8. First Milestone

The first practical milestone is:

**CoALA Persistent Memory Integration Test**

Expected workflow:

1. Start Python application.
2. User submits a question.
3. Python sends the request to Qwen through Ollama.
4. Qwen generates a response.
5. Python saves the question and response to Oracle.
6. Application terminates.
7. Application starts again.
8. Python retrieves the previous conversation from Oracle.

This verifies:
- Local model connectivity.
- Database connectivity.
- Persistence across application restarts.
- Basic separation between LLM and Agent memory.

However, this is only a preliminary integration test, not yet a complete CoALA agent.

---

## 9. My Learning Preferences

These are important. Follow them throughout the project.

1. Explain in Arabic (Moroccan Darija or clear Modern Standard Arabic).
2. Keep technical terminology in English.
3. Introduce English technical terms and explain their Arabic meanings.
4. Teach through project implementation rather than long abstract lectures.
5. Explain why each module exists.
6. Explain the design decisions before implementing them.
7. Write code incrementally, file by file.
8. Never dump the entire project implementation at once.
9. Explain every important function, class, and data structure.
10. Use practical tests after each implementation step.
11. Include expected outputs.
12. When errors occur, diagnose them instead of replacing everything with a new implementation.
13. Teach me the mathematical and algorithmic concepts when relevant.
14. Help me understand the implementation well enough to reproduce it independently.

I want to become capable of designing and implementing AI Agent architectures, not merely copying code.

---

## 10. Engineering Principles

- Modular architecture.
- Separation of concerns.
- Type hints.
- Pydantic validation.
- Logging.
- Unit and integration tests.
- Configuration through environment variables.
- Secure database credentials.
- Parameterized SQL.
- Explicit error handling.
- Reproducible experiments.
- Documentation.
- No unnecessary dependencies.
- Resource-efficient local execution.

Avoid giving an LLM unrestricted access to SQL, filesystem operations, or Python execution.

Implement an explicit permission system for tools.

Never assume that LLM-generated plans are correct.

Keep model inference separate from decision control and action execution.

---

## 11. Instructions for the New ChatGPT Session

Act as my AI research mentor, software architect, and implementation instructor.

We are continuing an existing project, not starting a new one.

First:
1. Read this entire handoff.
2. Understand the CoALA research framework.
3. Respect the current environment and installed software.
4. Do not repeat questions already answered here.
5. Do not restart the architectural discussion.
6. Do not switch to a different database or LLM runtime without justification.

Start by continuing **Phase 0**.

The immediate tasks are:

1. Verify the exact Qwen model tag using `ollama list`.
2. Confirm whether COALA_USER has been created.
3. If not, create it in FREEPDB1.
4. Set up the Python project directory and virtual environment.
5. Install `oracledb`, `requests`, `pydantic`, and `pytest`.
6. Implement and test the Oracle connection.
7. Implement and test the Ollama connection.

After successful integration tests, proceed to Phase 1.

**Important:** Work one step at a time. Give me executable commands, complete code for the current file, explanations in Arabic, and practical tests. Wait for my results before proceeding to the next dependent step.

The ultimate goal is to build a strong, research-oriented CoALA Research Agent with real persistent memory, reasoning, retrieval, learning, grounding, and controlled decision-making.