# IMAP Agent Building System

## 🚀 Overview

IMAP (Intelligent Multi-Agent Platform) Agent Building is an advanced platform designed to orchestrate AI-powered agents for automating web development projects from conception to deployment. The system leverages a team of specialized AI agents, each with defined roles and responsibilities, working collaboratively within the CrewAI framework.

The primary goal of IMAP is to significantly accelerate web development cycles, enhance code quality through automated processes, and allow human developers to focus on more complex and creative aspects of a project.

## ✨ Current Status (End of Initial Development & Testing Phase)

As of this version, the IMAP system has successfully demonstrated its core capabilities:

* **Multi-Agent Collaboration:** A team of agents (Project Manager, Researcher, Developer, Tester, Debugger) can execute sequential tasks.
* **Core Tooling Implemented:**
    * **File System Operations:** Agents can create, read, write, list, delete, move, and copy files and directories.
    * **Web Research:** Agents can perform web searches (via SerperDevTool) and scrape/summarize website content.
    * **Code Execution (Basic):**
        * Execution of JavaScript code via Node.js using a secure command executor tool.
        * Execution of Python code using CrewAI's `CodeInterpreterTool`.
    * **Browser Automation (Basic):** Agents can navigate web pages, extract content, and interact with elements using a direct Playwright Python API integration.
    * **Local HTTP Server:** Agents can start and stop a local HTTP server to serve and test locally generated web content.
* **Workflow Validation:** End-to-end workflows, including planning, development, local hosting, UI testing, and (mock) debugging, have been successfully tested with `gemini/gemini-1.5-flash` as the LLM for all agents.
* **Internal Communication:** Agent prompts, task descriptions, and tool documentation are designed for English as the primary internal communication language.

## 🛠️ Tech Stack (Core)

* **Python 3.12.10**
* **CrewAI & CrewAI-Tools:** For agent and task management. (Specific versions: `crewai==0.120.1`, `crewai-tools==0.45.0`)
* **LangChain (via CrewAI):** Underlying framework for LLM interactions. (Specific versions from your list, e.g., `langchain==0.3.25`, `langchain-core==0.3.60`)
* **Google Gemini Models:** Currently using `gemini/gemini-1.5-flash` via LiteLLM (configured through CrewAI's LLM wrapper). (`google-generativeai==0.6.18`, `langchain-google-genai==2.1.4`)
* **Playwright (Python sync_api):** For direct browser automation. (`playwright==1.52.0`)
* **Requests & BeautifulSoup4:** For web scraping. (`requests==2.32.3`, `beautifulsoup4==4.13.4`)
* **Docker (Python SDK):** For `CodeInterpreterTool` and potentially for future sandboxed execution of the `SecureCommandExecutorTool`. (`docker==7.1.0`)
* **ChromaDB:** For vector storage and retrieval. (`chromadb==0.5.23`)
* **Sentence-Transformers (often a dependency for ChromaDB/embeddings):** (`sentence-transformers` - version not in list, but often used with ChromaDB)
* **Standard Python Libraries:** `os`, `shutil`, `pathlib`, `subprocess`, `http.server`, `threading`, `socket`, `json`.
* **Environment Management:** `.venv` for virtual environments, `python-dotenv==1.1.0` for API key management.

## 🚀 Getting Started

1.  **Prerequisites:**
    * Python 3.12.10
    * Pip (usually comes with Python)
    * Git
    * Docker Desktop (or Docker Daemon) running (for `CodeInterpreterTool` and future sandboxing).
    * Node.js (for executing JavaScript examples).
    * Playwright browsers installed (`playwright install` in the venv).
2.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd imap-agent-system
    ```
3.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # .\.venv\Scripts\activate # Windows
    ```
4.  **Install Dependencies:**
    * It is highly recommended to generate a `requirements.txt` file from your current working environment:
      ```bash
      pip freeze > requirements.txt
      ```
    * Then install using:
      ```bash
      pip install -r requirements.txt
      ```
5.  **Set Up API Keys:**
    * Create a `.env` file in the project root.
    * Add your API keys:
        ```env
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        LITELLM_MODEL_NAME="gemini/gemini-1.5-flash" # Or your preferred Gemini model with prefix
        SERPER_API_KEY="YOUR_SERPER_API_KEY" # If using SerperDevTool
        ```
6.  **Run the Main Application:**
    * The main execution script is `main.py`. It contains various test workflows.
    * Execute a specific workflow by running:
        ```bash
        python main.py
        ```

## 📂 Project Structure

imap-agent-system/
├── .venv/                  # Virtual environment
├── agent_artifacts/        # Output from agent tasks (plans, reports - usually gitignored)
├── application_code/       # Code generated by agents for target projects (usually gitignored)
├── tools/                  # Custom tools for agents
│   ├── init.py
│   ├── file_operations_tool.py
│   ├── web_tools.py
│   ├── execution_tools.py
│   └── server_tools.py
├── agents.py               # Definitions of all specialized agents
├── main.py                 # Main script to run crews and test workflows
├── .env                    # API keys and environment variables (gitignored)
├── .gitignore
├── requirements.txt        # Generated list of Python dependencies
├── README.md               # This file
├── SYSTEM_OVERVIEW.md      # Detailed system architecture and design
└── VISION_AND_NEXT_STEPS.md # Project vision and future development

## 🤝 Contributing

Fabian, Gemini & Claude

## 📜 License

(To be defined)
