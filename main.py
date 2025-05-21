import os
import json
from dotenv import load_dotenv
from crewai import Task, Crew, Process
import time 

# Load environment variables FIRST
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY nicht in .env gefunden! Bitte in der .env Datei eintragen.")

os.environ["GEMINI_API_KEY"] = gemini_api_key
os.environ["GOOGLE_API_KEY"] = gemini_api_key

lite_llm_model_name = os.getenv("LITELLM_MODEL_NAME", "gemini/gemini-1.5-flash")
os.environ["LITELLM_MODEL_NAME"] = lite_llm_model_name

serper_api_key = os.getenv("SERPER_API_KEY")
if serper_api_key:
    os.environ["SERPER_API_KEY"] = serper_api_key
else:
    print("WARNUNG: SERPER_API_KEY nicht in .env gefunden!")

from agents import project_manager_agent, developer_agent, tester_agent
from tools.web_tools import close_browser_tool
from tools.server_tools import stop_local_http_server_tool, is_port_available # is_port_available importiert

base_project_path = "test_project_local_host_v2" 
artifacts_path = os.path.join(base_project_path, "agent_artifacts")
application_code_path = os.path.join(base_project_path, "application_code") 

pm_dev_plan_file = os.path.join(artifacts_path, "dev_plan_local_test.md")
app_html_file_name = "index.html"
app_html_file_path = os.path.join(application_code_path, app_html_file_name)
tester_ui_test_plan_file = os.path.join(artifacts_path, "tester_ui_test_plan.md")
tester_results_file = os.path.join(artifacts_path, "tester_ui_results.txt")

local_server_port = 8088 

task_pm_plan_html = Task(
    description=(
        f"You are the Project Manager. Create a development plan for the Developer Agent. "
        f"The plan should instruct the Developer to create a very simple HTML file named '{app_html_file_name}' "
        f"in the directory '{application_code_path}'.\n"
        f"The HTML content should be:\n"
        f"```html\n"
        f"<!DOCTYPE html>\n"
        f"<html>\n<head><title>My Test Page</title></head>\n"
        f"<body><h1>Welcome to My Test Page</h1><p>This is a test paragraph.</p></body>\n"
        f"</html>\n"
        f"```\n"
        f"1. Ensure the directory '{application_code_path}' is created if it doesn't exist.\n"
        f"2. Write the development plan into the file '{pm_dev_plan_file}'."
    ),
    expected_output=f"Confirmation that the development plan for '{app_html_file_name}' has been written to '{pm_dev_plan_file}'. Include the plan content.",
    agent=project_manager_agent
)

task_dev_create_html = Task(
    description=(
        f"You are the Developer. Read the development plan from '{pm_dev_plan_file}'.\n"
        f"Precisely follow the plan to create the directory '{application_code_path}' (if needed) "
        f"and the HTML file '{app_html_file_path}' with the specified content."
    ),
    expected_output=f"Confirmation that the HTML file '{app_html_file_path}' has been created with the correct content.",
    agent=developer_agent,
    context=[task_pm_plan_html]
)

task_pm_plan_ui_test = Task(
    description=(
        f"You are the Project Manager. The Developer has created '{app_html_file_path}'. "
        f"This file will be served by a local HTTP server from the '{application_code_path}' directory on port {local_server_port} "
        f"(URL: http://localhost:{local_server_port}/{app_html_file_name}).\n"
        f"Create a test plan for the QA Engineer (Tester Agent) to verify this locally hosted page.\n"
        f"The plan should instruct the Tester to:\n"
        f"1. Use the 'Start Local HTTP Server Tool' to serve files from '{application_code_path}' on port {local_server_port}.\n"
        f"2. Use the 'Navigate Browser Tool' to open 'http://localhost:{local_server_port}/{app_html_file_name}'.\n"
        f"3. Use the 'Get Page Content Tool' to retrieve the text of the 'h1' element.\n"
        f"4. Use the 'Get Page Content Tool' to retrieve the text of the 'p' element.\n"
        f"5. Verify that the h1 text is 'Welcome to My Test Page' and the p text is 'This is a test paragraph.'.\n"
        f"6. Write a test report into '{tester_results_file}' indicating PASSED (with retrieved texts) or FAILED (with reasons).\n"
        f"7. Use the 'Close Browser Tool'.\n"
        f"8. Use the 'Stop Local HTTP Server Tool'.\n"
        f"Write this UI test plan into '{tester_ui_test_plan_file}'."
    ),
    expected_output=f"Confirmation that the UI test plan has been written to '{tester_ui_test_plan_file}'. Include the plan content.",
    agent=project_manager_agent,
    context=[task_dev_create_html]
)

task_tester_execute_ui_test = Task(
    description=(
        f"You are the QA Engineer. Read your UI test plan from '{tester_ui_test_plan_file}'.\n"
        f"Execute the steps precisely:\n"
        f"1. Start the local HTTP server to serve from '{os.path.abspath(application_code_path)}' on port {local_server_port} using 'Start Local HTTP Server Tool'. Confirm it started.\n" 
        f"2. Navigate to 'http://localhost:{local_server_port}/{app_html_file_name}' using 'Navigate Browser Tool'.\n"
        f"3. Get h1 text using 'Get Page Content Tool' (selector 'h1'). Store as 'h1_text'.\n"
        f"4. Get paragraph text using 'Get Page Content Tool' (selector 'p'). Store as 'p_text'.\n"
        f"5. Compare 'h1_text' with 'Welcome to My Test Page' and 'p_text' with 'This is a test paragraph.'.\n"
        f"6. Create a report: 'UI Test Report: H1: [h1_text], P: [p_text]. Test Result: [PASSED/FAILED]. Reason: [If FAILED, explain why]'.\n"
        f"7. Write this report to '{tester_results_file}' using 'Write File Tool'.\n"
        f"8. Close the browser using 'Close Browser Tool'.\n"
        f"9. Stop the local HTTP server using 'Stop Local HTTP Server Tool'."
    ),
    expected_output=(
        f"Confirmation that the UI test was executed, results written to '{tester_results_file}', "
        f"browser closed, and HTTP server stopped. Include the content of '{tester_results_file}'."
    ),
    agent=tester_agent,
    context=[task_pm_plan_ui_test]
)

local_test_crew = Crew(
    agents=[project_manager_agent, developer_agent, tester_agent],
    tasks=[
        task_pm_plan_html,
        task_dev_create_html,
        task_pm_plan_ui_test,
        task_tester_execute_ui_test
    ],
    process=Process.sequential,
    verbose=True
)

def setup_local_test_environment():
    os.makedirs(artifacts_path, exist_ok=True)
    os.makedirs(application_code_path, exist_ok=True) 
    print(f"Basis-Verzeichnisse für Local Host Test '{base_project_path}' sichergestellt/erstellt.")

if __name__ == '__main__':
    print(f"Starte Local Host UI Test-Crew (Port {local_server_port})...")
    setup_local_test_environment()

    if not is_port_available(local_server_port): 
        print(f"FEHLER: Port {local_server_port} ist bereits belegt! Bitte Skript beenden und Port freigeben oder ändern.")
        exit()

    for agent_instance in local_test_crew.agents:
        if agent_instance.llm and hasattr(agent_instance.llm, 'model'):
            print(f"Agent '{agent_instance.role}' LLM Modell: {agent_instance.llm.model}")
    
    print(f"PM Dev Plan wird in '{pm_dev_plan_file}' erwartet.")
    print(f"Developer HTML Output in '{app_html_file_path}'.")
    print(f"PM UI Test Plan in '{tester_ui_test_plan_file}'.")
    print(f"Tester UI Test Ergebnis in '{tester_results_file}'.")

    try:
        result = local_test_crew.kickoff()
        print("\n\n########################")
        print("## Ergebnis der Local Host UI Test-Crew:")
        print(result) 
        print("########################")

        print("\n--- Manuelle Überprüfung der erstellten Dateien ---")
        files_to_check = {
            "PM Dev Plan": pm_dev_plan_file,
            "Developer HTML File": app_html_file_path,
            "PM UI Test Plan": tester_ui_test_plan_file,
            "Tester UI Test Results": tester_results_file,
        }
        for name, file_path_to_check in files_to_check.items():
            if os.path.exists(file_path_to_check):
                print(f"\nInhalt von '{name}' ({file_path_to_check}):")
                with open(file_path_to_check, "r", encoding="utf-8") as f:
                    print(f.read())
            else:
                print(f"Datei '{name}' ({file_path_to_check}) wurde NICHT gefunden.")
        
    except Exception as e:
        print(f"\nEin Fehler ist während der Local Host UI Test-Crew-Ausführung aufgetreten: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n--- Versuche abschließendes Aufräumen (Browser und HTTP Server)... ---")
        try:
            # KORRIGIERTER AUFRUF für Tools ohne Argumente
            browser_cleanup_msg = close_browser_tool.run() 
            print(f"Aufräum-Nachricht für Browser: {browser_cleanup_msg}")
        except Exception as ex_browser:
            print(f"Fehler beim expliziten Aufräumen des Browsers: {ex_browser}")
        
        time.sleep(0.5) 
        
        try:
            # KORRIGIERTER AUFRUF für Tools ohne Argumente
            server_cleanup_msg = stop_local_http_server_tool.run() 
            print(f"Aufräum-Nachricht für HTTP Server: {server_cleanup_msg}")
        except Exception as ex_server:
            print(f"Fehler beim expliziten Aufräumen des HTTP Servers: {ex_server}")

