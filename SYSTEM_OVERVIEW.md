IMAP Agent Building System - System Overview

This document provides a detailed overview of the architecture, agent roles, workflow, and design decisions for the IMAP Agent Building System.
1. Core Architecture

The IMAP Agent Building System is a multi-agent platform built using Python (specifically Python 3.12.10) and the CrewAI framework. It is designed to automate various stages of web development projects.

    Framework: CrewAI (crewai==0.120.1) is used for defining agents, tasks, tools, and orchestrating their execution in crews. crewai-tools==0.45.0 provides a set of pre-built tools and base classes.

    Language Model (LLM) Integration:

        The system is designed to be flexible with LLM choices. Currently, for development and testing, it's configured to use Google's Gemini models (specifically gemini/gemini-1.5-flash as defined by the LITELLM_MODEL_NAME environment variable) via CrewAI's LLM wrapper, which utilizes LiteLLM (litellm==1.68.0) internally.

        The google-generativeai==0.6.18 and langchain-google-genai==2.1.4 libraries facilitate the interaction with Gemini models.

        API keys are managed through a .env file (loaded by python-dotenv==1.1.0) and environment variables.

    Modularity: The system is structured with clear separation between:

        Agent definitions (agents.py).

        Tool implementations (in the tools/ directory, categorized by function).

        Workflow definitions and execution logic (main.py).

    Communication:

        Internal Agent Communication: Primarily English for prompts, task descriptions, and tool interactions.

        User-Facing Output: Designed to be in German.

        Inter-Agent Data Exchange: Primarily through files and task context in CrewAI.

2. Agent Roles and Responsibilities

The system employs a team of specialized AI agents. Currently, all agents use gemini/gemini-1.5-flash for development and testing. The target LLMs for the final, production-ready version are:

    Project Manager (PM) Agent:

        LLM Target (Final): Gemini 2.5 Pro.

        Responsibilities: User interaction, strategic planning, task breakdown, coordination. Loads the full relevant context of the current project state at the beginning of each planning step.

        Key Tools: File operations, (future) Gemini Vision, SerperDevTool, Scrape Website Content Tool.

    Researcher Agent:

        LLM Target (Final): Gemini 1.5 Flash.

        Responsibilities: Market analysis, technology benchmarking, information gathering. Agents are instructed to use research tools when faced with uncertainty rather than speculating.

        Key Tools: SerperDevTool (crewai-tools), Scrape Website Content Tool, File Write Tool.

    Developer Agent:

        LLM Target (Final): Gemini 2.5 Pro.

        Responsibilities: Code implementation, file manipulation, script execution.

        Key Tools: File operations, Secure Command Executor Tool, CodeInterpreterTool (crewai-tools).

    Tester Agent:

        LLM Target (Final): Mistral Medium.

        Responsibilities: Test plan creation, execution (CLI scripts, UI browser automation), bug reporting.

        Key Tools: File operations, Secure Command Executor Tool, CodeInterpreterTool, Playwright Browser Tools, Local HTTP Server Tools.

    Debug Agent:

        LLM Target (Final): Codestral.

        Responsibilities: Analysis of failed tests, root cause identification, proposing fixes.

        Key Tools: File operations, Secure Command Executor Tool, CodeInterpreterTool, Playwright Browser Tools.

3. Core Implemented Tools

    File Operations (tools/file_operations_tool.py):

        Provides: write_file_tool, read_file_tool, create_directory_tool, list_directory_contents_tool, delete_file_tool, delete_directory_tool, move_path_tool, copy_path_tool.

        Implementation: Python's os, shutil, pathlib.

    Web Tools (tools/web_tools.py):

        scrape_website_content_tool: Fetches text from URLs using requests==2.32.3 and beautifulsoup4==4.13.4.

        navigate_browser_tool, get_page_content_tool, click_element_tool, type_text_tool, close_browser_tool: Direct Playwright (playwright==1.52.0) Python API integration.

    Execution Tools (tools/execution_tools.py):

        secure_command_executor_tool: Executes system commands via subprocess.

        CodeInterpreterTool (from crewai_tools): Leverages Docker (docker==7.1.0 Python SDK).

    Server Tools (tools/server_tools.py):

        start_local_http_server_tool, stop_local_http_server_tool: Uses Python's http.server, socketserver, threading. Includes port check via socket.

    Vector Storage (Planned):

        ChromaDB (chromadb==0.5.23) is installed for future use in long-term memory and RAG.

4. Workflow (Conceptual - as tested)

(Content remains the same as in Immersive IMAP_Project_Plan_V2)
5. Key Design Decisions and Principles

    Direct Playwright Integration: Moved away from Docker/MCP for Playwright to a direct Python API integration for simplicity and robustness.

    Agent-Led Summarization: For web scraping, the tool provides raw text, and the agent itself is responsible for summarization using its LLM. (Note: The alternative of tool-based summarization is kept in mind for future, more advanced LLMs).

    Explicit Tool Usage in Tasks: Task descriptions are crafted to guide agents on which tools to use for specific sub-steps.

    File-Based Artifact Exchange: Agents primarily exchange complex information via files.

    Iterative Tool Development: Tools are built incrementally.

    Internal English Communication: Standardized for better LLM performance.

    Agent Behavior Principle: Agents are designed and prompted to utilize their research tools when faced with uncertainty or lack of information, rather than speculating or "hallucinating" solutions.

    Modular Tools: Tools are designed to be relatively self-contained.

6. Management of Sensitive Information

(Content remains the same as in Immersive IMAP_Project_Plan_V2)

This overview should provide a solid understanding of the IMAP system's current architecture and design.