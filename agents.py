import os
from dotenv import load_dotenv # HINZUGEFÜGT
from crewai import Agent, LLM
from crewai_tools import SerperDevTool, CodeInterpreterTool 

# Import file system tools
from tools.file_operations_tool import (
    write_file_tool,
    read_file_tool,
    create_directory_tool,
    list_directory_contents_tool,
    delete_file_tool,
    delete_directory_tool,
    move_path_tool,
    copy_path_tool
)

# Import web tools
from tools.web_tools import (
    scrape_website_content_tool,
    navigate_browser_tool, 
    get_page_content_tool,
    click_element_tool,      
    type_text_tool,          
    close_browser_tool       
)

# Import execution tools
from tools.execution_tools import secure_command_executor_tool

# Import server tools
from tools.server_tools import ( 
    start_local_http_server_tool,
    stop_local_http_server_tool
)

# Import Vision Analyzer Tool
from tools.vision_analyzer_tool import gemini_vision_analyzer_tool

# Umgebungsvariablen laden, BEVOR sie verwendet werden
load_dotenv() 

gemini_api_key = os.getenv("GEMINI_API_KEY")
lite_llm_model_name = os.getenv("LITELLM_MODEL_NAME") 

if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in environment variables. "
        "Ensure .env is loaded and the key is set (e.g., in .env file or main.py)."
    )
if not lite_llm_model_name:
    raise ValueError(
        "LITELLM_MODEL_NAME not found in environment variables. "
        "Ensure it is set (e.g., in .env file or main.py, e.g., 'gemini/gemini-1.5-flash')."
    )

try:
    default_llm = LLM(
        model=lite_llm_model_name, # KORRIGIERT: model_name zu model geändert
        api_key=gemini_api_key
    )
    print(f"--- Debug (Agents): Default LLM for agents initialized with model: {lite_llm_model_name} ---")
except Exception as e:
    print(f"Error initializing default_llm in agents.py: {e}")
    default_llm = None

# --- Project Manager Agent ---
project_manager_agent = Agent(
    role="Senior Web Development Project Manager",
    goal=(
        "Lead and coordinate web development projects from conception to completion. "
        "Ensure all requirements are met, and the project is delivered on time and to a high standard. "
        "Analyze design mockups using vision tools to inform planning." 
    ),
    backstory=(
        "You are a highly skilled project manager with over 10 years of experience leading complex web development projects. "
        "You are an expert in agile methodologies, requirements analysis, risk management, and team coordination. "
        "You communicate clearly and concisely, making informed decisions to drive projects to success. "
        "You utilize file system tools to create and manage plans, research tools to gather information, "
        "and vision tools to understand visual designs." 
    ),
    verbose=True,
    allow_delegation=True, 
    tools=[
        write_file_tool,
        read_file_tool,
        create_directory_tool,
        list_directory_contents_tool,
        delete_file_tool,
        delete_directory_tool,
        move_path_tool,
        copy_path_tool,
        SerperDevTool(), 
        scrape_website_content_tool,
        gemini_vision_analyzer_tool 
    ],
    llm=default_llm
)

# --- Developer Agent ---
developer_agent = Agent(
    role="Senior Full-Stack Web Developer",
    goal="Implement features, components, and file structures for web applications precisely as planned by the Project Manager. Execute code and scripts as needed, including Python scripts.",
    backstory=(
        "You are an experienced Full-Stack Developer with expertise in various web technologies (HTML, CSS, JavaScript, Python, etc.). "
        "You are known for clean, efficient, and well-documented code. You read plans carefully and implement them exactly. "
        "You use file system tools to create and modify code files and directories, and execution tools (like a command executor or a Python code interpreter) to run and test your code."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[
        write_file_tool,
        read_file_tool,
        create_directory_tool,
        list_directory_contents_tool,
        delete_file_tool,
        delete_directory_tool,
        move_path_tool,
        copy_path_tool,
        secure_command_executor_tool,
        CodeInterpreterTool() 
    ],
    llm=default_llm
)

# --- Researcher Agent ---
researcher_agent = Agent(
    role="Professional Research Specialist and Analyst",
    goal="Conduct comprehensive and targeted research on given topics, extract relevant information from websites, and summarize it concisely.",
    backstory=(
        "You are an expert in information retrieval and analysis. You can efficiently use web search engines "
        "to identify relevant sources. Subsequently, you are adept at extracting, evaluating, "
        "and synthesizing the core insights from these sources into a clear and understandable format. "
        "You ensure to use only trustworthy information and structure your findings well."
    ),
    verbose=True,
    allow_delegation=False, 
    tools=[
        SerperDevTool(), 
        scrape_website_content_tool, 
        write_file_tool 
    ],
    llm=default_llm
)

# --- Tester Agent ---
tester_agent = Agent(
    role="Meticulous Quality Assurance Engineer",
    goal="Ensure the quality and functionality of web applications by creating and executing test plans, running code or test scripts, performing browser-based UI tests on local or remote servers, and meticulously documenting any found issues.",
    backstory=(
        "You are a detail-oriented QA Engineer with a passion for finding bugs and ensuring software quality. "
        "You are proficient in creating comprehensive test plans based on project requirements and implemented features. "
        "You can execute various types of tests, including running command-line test scripts and performing UI tests using browser automation. "
        "You can start and stop local HTTP servers to test web applications served from local directories. "
        "You provide clear, actionable bug reports or test summaries. "
        "You use file system tools to read plans/code and write test reports, execution tools to run tests, browser tools for UI testing, and server tools for local hosting."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[
        read_file_tool,    
        write_file_tool,   
        list_directory_contents_tool,
        secure_command_executor_tool,
        CodeInterpreterTool(),
        navigate_browser_tool,      
        get_page_content_tool,    
        click_element_tool,       
        type_text_tool,           
        close_browser_tool,
        start_local_http_server_tool, 
        stop_local_http_server_tool   
    ],
    llm=default_llm
)

# --- Debug Agent ---
debug_agent = Agent(
    role="Expert Software Debugger and Problem Solver",
    goal="Analyze issues reported by the Tester Agent, identify root causes by examining code, logs, and browser states, and propose or implement effective solutions and fixes.",
    backstory=(
        "You are a seasoned software debugger with a knack for quickly understanding complex code and pinpointing the source of errors. "
        "You can analyze test results, logs, and code to diagnose problems. You can also inspect web page states if needed. "
        "You are skilled in formulating clear explanations of issues and suggesting precise code modifications or other fixes. "
        "You use file system tools to read relevant files and write your analysis or proposed fixes. You may also use execution or browser tools to verify fixes."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[
        read_file_tool,    
        write_file_tool,   
        list_directory_contents_tool,
        secure_command_executor_tool,
        CodeInterpreterTool(),
        navigate_browser_tool,    
        get_page_content_tool,  
        click_element_tool,     
        type_text_tool,         
        close_browser_tool      
    ],
    llm=default_llm
)

if __name__ == '__main__':
    if default_llm:
        print("Default LLM in agents.py initialized successfully.")
        # Sicherer Zugriff auf model Attribut, falls es bei LiteLLM anders heißt
        llm_model_display_name = getattr(default_llm, 'model', getattr(default_llm, 'model_name', 'N/A'))
        print(f"Configured model for default_llm: {llm_model_display_name}")


        agent_list = [
            ("Project Manager Agent", project_manager_agent),
            ("Developer Agent", developer_agent),
            ("Researcher Agent", researcher_agent),
            ("Tester Agent", tester_agent),
            ("Debug Agent", debug_agent)
        ]

        for name, agent_instance in agent_list:
            print(f"\n--- {name} ---")
            print(f"Role: {agent_instance.role}")
            if agent_instance.tools:
                print(f"Tools: {[tool.name for tool in agent_instance.tools]}")
            else:
                print("Tools: None")
    else:
        print("Default LLM could NOT be initialized in agents.py.")
