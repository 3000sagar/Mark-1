# MARK-1 🚀

Local Autonomous AI Development Assistant

---

## 🔥 Overview

MARK-1 is a local AI agent capable of:

- Reading and writing files
- Executing terminal commands
- Planning multi-step tasks
- Autonomous goal execution
- Memory-based reasoning
- Error recovery with replanning

---

## 🧠 Architecture

- Planner → Converts user input into steps
- Executor → Executes tools safely
- Tool System → File + Terminal operations
- Memory → Context-aware reasoning
- Goal Engine → Autonomous execution loop

---

## ⚙️ Features

- Multi-step task execution
- Autonomous goal mode (`goal <task>`)
- Intelligent tool usage
- Context-aware responses
- Secure workspace sandbox

---

## 🚀 Usage

```bash
python mark1.py



mark1/
│
├── mark1.py
├── pyproject.toml
├── requirements.txt
├── README.md
├── .env
│
├── config/
│   ├── settings.yaml
│   ├── models.yaml
│   └── tools.yaml
│
├── core/
│   ├── orchestrator.py
│   ├── planner.py
│   ├── executor.py
│   ├── task_manager.py
│   └── state_manager.py
│
├── runtime/
│   ├── cli.py
│   ├── command_handler.py
│   └── session.py
│
├── tools/
│   ├── base_tool.py
│   ├── file_tools.py
│   ├── terminal_tools.py
│   ├── project_tools.py
│   └── tool_registry.py
│
├── models/
│   ├── llm_interface.py
│   ├── ollama_model.py
│   └── embedding_model.py
│
├── memory/
│   ├── short_term_memory.py
│   ├── long_term_memory.py
│   ├── vector_store.py
│   └── memory_manager.py
│
├── workspace/
│   ├── projects/
│   └── temp/
│
├── logs/
│   ├── agent.log
│   └── actions.log
│
├── storage/
│   ├── tasks/
│   ├── sessions/
│   └── embeddings/
│
├── security/
│   ├── sandbox.py
│   ├── permission_manager.py
│   └── command_whitelist.py
│
├── utils/
│   ├── logger.py
│   ├── file_utils.py
│   ├── parser.py
│   └── validators.py
│
├── prompts/
│   ├── planner_prompt.txt
│   ├── executor_prompt.txt
│   └── system_prompt.txt
│
└── tests/
    ├── test_tools.py
    ├── test_executor.py
    ├── test_memory.py
    └── test_models.py