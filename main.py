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
# GOOGLE_API_KEY wird oft von LangChain oder anderen Google-Bibliotheken intern verwendet,
# daher ist es gut, ihn auch zu setzen, oft ist er identisch mit dem GEMINI_API_KEY für Gemini-Modelle.
os.environ["GOOGLE_API_KEY"] = gemini_api_key 

lite_llm_model_name = os.getenv("LITELLM_MODEL_NAME", "gemini/gemini-1.5-flash")
os.environ["LITELLM_MODEL_NAME"] = lite_llm_model_name

serper_api_key = os.getenv("SERPER_API_KEY")
if serper_api_key:
    os.environ["SERPER_API_KEY"] = serper_api_key
else:
    print("WARNUNG: SERPER_API_KEY nicht in .env gefunden!")

from agents import project_manager_agent, developer_agent, tester_agent # researcher_agent, debug_agent (falls benötigt)
from tools.web_tools import close_browser_tool
from tools.server_tools import stop_local_http_server_tool, is_port_available 

# --- Pfaddefinitionen ---
# Basis-Projektpfad für Artefakte und generierten Code
# Es ist eine gute Praxis, diesen Pfad relativ zum main.py Skript zu definieren
# oder sicherzustellen, dass er immer vom Projekt-Root aus korrekt aufgelöst wird.
script_dir = os.path.dirname(__file__)
base_project_path = os.path.join(script_dir, "test_project_vision_tool") # Eigener Ordner für diesen Test
artifacts_path = os.path.join(base_project_path, "agent_artifacts")
application_code_path = os.path.join(base_project_path, "application_code") 

# Pfad zum Testbild (angenommen im Projekt-Root/test_images)
# Passe dies an, falls dein Bild woanders liegt.
test_image_for_pm_analysis = os.path.join(script_dir, "test_images", "test_mockup.png") 
pm_vision_analysis_report_file = os.path.join(artifacts_path, "pm_vision_analysis_report.md")


# --- Bestehende Task-Definitionen (Beispielhaft gekürzt, deine Originale bleiben) ---
# Du hattest hier task_pm_plan_html, task_dev_create_html etc.
# Diese lasse ich für die Übersichtlichkeit hier weg, aber sie bleiben in deiner Datei.

# --- NEUE TASK UND CREW FÜR VISION TOOL TEST ---

task_pm_analyze_mockup = Task(
    description=(
        f"You are the Project Manager. Your task is to analyze a UI mockup image. "
        f"The image is located at the path: '{test_image_for_pm_analysis}'.\n"
        f"1. Use the 'Gemini Vision Analyzer Tool' to analyze this image.\n"
        f"2. For the analysis prompt, use the following: 'Thoroughly describe all UI elements visible in this mockup. "
        f"Identify the overall layout, color scheme, typography, and any interactive elements suggested by the design. "
        f"Extract any visible text content. Note the perceived style or branding.'\n"
        f"3. After receiving the analysis, write a comprehensive report based on the analysis text. "
        f"The report should summarize the findings clearly.\n"
        f"4. Save this report to the file: '{pm_vision_analysis_report_file}' using the 'Write File Tool'."
    ),
    expected_output=(
        f"A confirmation that the UI mockup analysis has been completed and the detailed report "
        f"has been successfully written to '{pm_vision_analysis_report_file}'. "
        f"Include the full content of the written report in your final output."
    ),
    agent=project_manager_agent,
    # tools=[gemini_vision_analyzer_tool, write_file_tool] # Tools sind bereits beim Agenten registriert
)

vision_test_crew = Crew(
    agents=[project_manager_agent],
    tasks=[task_pm_analyze_mockup],
    process=Process.sequential,
    verbose=True
)

# --- Ende: NEUE TASK UND CREW FÜR VISION TOOL TEST ---


def setup_test_environment(base_path, artifacts_subpath, app_code_subpath):
    """Stellt sicher, dass die Basisverzeichnisse für Tests existieren."""
    os.makedirs(artifacts_subpath, exist_ok=True)
    os.makedirs(app_code_subpath, exist_ok=True) 
    print(f"Basis-Verzeichnisse für Test '{base_path}' sichergestellt/erstellt.")

if __name__ == '__main__':
    print("Starte IMAP Agent System...")
    
    # Setup für die neue Vision-Test-Crew
    setup_test_environment(base_project_path, artifacts_path, application_code_path)

    print(f"\n--- Starte Vision Test Crew ---")
    print(f"Project Manager soll Bild analysieren: '{test_image_for_pm_analysis}'")
    print(f"Analysebericht erwartet in: '{pm_vision_analysis_report_file}'")

    # Überprüfen, ob das Testbild existiert, bevor die Crew gestartet wird
    if not os.path.exists(test_image_for_pm_analysis):
        print(f"FEHLER: Das Testbild '{test_image_for_pm_analysis}' wurde nicht gefunden!")
        print("Bitte stelle sicher, dass das Bild im Ordner 'test_images' im Projekt-Root liegt oder passe den Pfad an.")
    else:
        try:
            vision_result = vision_test_crew.kickoff()
            print("\n\n########################")
            print("## Ergebnis der Vision Test Crew:")
            print(vision_result)
            print("########################")

            if os.path.exists(pm_vision_analysis_report_file):
                print(f"\n--- Inhalt des Analyseberichts ({pm_vision_analysis_report_file}): ---")
                with open(pm_vision_analysis_report_file, "r", encoding="utf-8") as f:
                    print(f.read())
            else:
                print(f"FEHLER: Der Analysebericht '{pm_vision_analysis_report_file}' wurde nicht erstellt.")

        except Exception as e:
            print(f"\nEin Fehler ist während der Ausführung der Vision Test Crew aufgetreten: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Hier könnten spezifische Aufräumarbeiten für diese Crew stehen, falls nötig
            print("\n--- Vision Test Crew abgeschlossen. ---")

    # Hier könntest du deine ursprüngliche local_test_crew oder andere Crews auch noch ausführen lassen.
    # Für diesen Test fokussieren wir uns auf die vision_test_crew.
    # print("\n--- Starte ursprüngliche Local Host UI Test-Crew (Beispiel) ---")
    # ... (dein Code für die andere Crew) ...

    print("\n--- Alle Testläufe (falls mehrere) abgeschlossen. ---")
