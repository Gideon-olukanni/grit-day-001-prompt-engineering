"""
GRIT — Day 1 of 1825
Prompt Engineering Workflow Tester — Cycle 1
AI & Automation | August 17, 2026

Purpose:
    Implements the seven-stage prompt engineering workflow as a
    command-line tool. Run this script, enter a task and prompt,
    and it guides you through definition, testing, evaluation,
    and documentation — producing a structured record at the end.

Usage:
    python3 prompt_tester.py

Requirements:
    Python 3.7+ | No external libraries | No API key needed
    (Day 1 uses local simulation. API integration arrives in Cycle 3.)
"""

import json
import datetime
import os


# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────

EVALUATION_CRITERIA = [
    "Task completion — did the output do exactly what you asked?",
    "Format compliance — is the output in the correct format?",
    "Accuracy — is the content factually correct?",
    "Tone — is the style appropriate for the audience?",
    "Length — is the output the right length?",
    "Usefulness — would you actually use this output?",
]

PROMPT_COMPONENTS = [
    "Context (background the model needs)",
    "Task (action verb + specific instruction)",
    "Format (structure of the output)",
    "Constraints (rules the output must follow)",
    "Role (persona for the model)",
    "Examples (demonstrations of the pattern)",
    "Tone (stylistic register)",
    "Negative instructions (what NOT to do)",
]

WORKFLOW_STAGES = [
    "DEFINE",
    "DRAFT",
    "TEST",
    "EVALUATE",
    "REFINE",
    "DOCUMENT",
    "REUSE",
]


# ─────────────────────────────────────────────────────────────
# DISPLAY HELPERS
# ─────────────────────────────────────────────────────────────

def divider(char="─", width=60):
    print(char * width)


def header(text):
    print()
    divider("═")
    print(f"  {text}")
    divider("═")


def stage_header(number, name):
    print()
    divider()
    print(f"  STAGE {number} — {name}")
    divider()


def prompt_input(label):
    """Multi-line input. Press Enter twice to finish."""
    print(f"\n{label}")
    print("(Press Enter twice to finish)")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    # Remove trailing blank lines
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def score_input(label, minimum=1, maximum=5):
    """Validated score input."""
    while True:
        raw = input(f"  {label} [{minimum}–{maximum}]: ").strip()
        try:
            value = int(raw)
            if minimum <= value <= maximum:
                return value
            print(f"  Enter a number between {minimum} and {maximum}.")
        except ValueError:
            print("  Enter a number.")


def yes_no(prompt_text):
    while True:
        raw = input(f"\n{prompt_text} [y/n]: ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  Enter y or n.")


# ─────────────────────────────────────────────────────────────
# STAGE IMPLEMENTATIONS
# ─────────────────────────────────────────────────────────────

def stage_define():
    """Stage 1: Guide the user through task definition."""
    stage_header(1, "DEFINE")
    print("""
Before writing your prompt, answer these five questions.
The quality of your prompt depends on the clarity of your answers.
""")
    definition = {}

    questions = [
        ("output", "1. What specific output do you want?"),
        ("audience", "2. Who is the audience for this output?"),
        ("format", "3. What format should the output take?"),
        ("constraints", "4. What are the constraints?"),
        ("success_criteria", "5. How will you know if the output is good?"),
    ]

    for key, question in questions:
        print(f"\n{question}")
        definition[key] = input("   → ").strip()

    print("\nYour task definition:")
    for key, question in questions:
        print(f"  {question}\n     {definition[key]}")

    return definition


def stage_draft(definition):
    """Stage 2: Guide the user through drafting the prompt."""
    stage_header(2, "DRAFT")
    print("""
Write your prompt. Use any of these eight components:

  Context · Task · Format · Constraints
  Role · Examples · Tone · Negative instructions

Your task: """ + definition["output"] + "\nAudience: " + definition["audience"])

    prompt_text = prompt_input("\nYour prompt draft:")

    # Check which components are present
    print("\nComponent check — which components did you include?")
    present_components = []
    for component in PROMPT_COMPONENTS:
        if yes_no(f"  {component}?"):
            present_components.append(component)

    missing = [c for c in PROMPT_COMPONENTS if c not in present_components]
    if missing:
        print("\nMissing components (consider adding for next iteration):")
        for m in missing:
            print(f"  → {m}")
    else:
        print("\nAll eight components present. Strong draft.")

    return {"prompt": prompt_text, "components_present": present_components}


def stage_test(draft):
    """Stage 3: Run the prompt (manual in Cycle 1)."""
    stage_header(3, "TEST")
    print("""
Your prompt is ready to run. In Cycle 1 (Day 1), you will:
  1. Copy the prompt below
  2. Paste it into Claude, ChatGPT, or another LLM
  3. Read the ENTIRE output before evaluating

Your prompt:
""")
    divider("-")
    print(draft["prompt"])
    divider("-")

    input("\nPress Enter when you have read the complete output...")

    output_summary = prompt_input("\nPaste or summarise the model's output:")

    return {"output": output_summary}


def stage_evaluate(definition, result):
    """Stage 4: Evaluate the output against criteria."""
    stage_header(4, "EVALUATE")
    print("""
Score the output 1–5 for each criterion.
1 = completely failed | 5 = perfect

Be specific in your notes — not 'bad', but 'wrong format because used
bullets instead of paragraphs'.
""")

    scores = {}
    notes = {}
    for criterion in EVALUATION_CRITERIA:
        print(f"\n  {criterion}")
        score = score_input("Score")
        note = input("  Note (what specifically worked or failed): ").strip()
        scores[criterion] = score
        notes[criterion] = note

    total = sum(scores.values())
    average = total / len(scores)
    print(f"\nTotal score: {total}/{len(scores) * 5}")
    print(f"Average: {average:.1f}/5")

    if average >= 4.5:
        print("Excellent output. Document and move to reuse.")
    elif average >= 3.5:
        print("Good output. Minor refinements needed.")
    elif average >= 2.5:
        print("Mediocre output. Significant refinement needed.")
    else:
        print("Poor output. Rethink the approach. Return to Stage 1.")

    return {
        "scores": scores,
        "notes": notes,
        "average": round(average, 2),
        "success_criteria": definition["success_criteria"],
    }


def stage_refine(draft, evaluation):
    """Stage 5: Guide a single-change refinement."""
    stage_header(5, "REFINE")

    # Find the lowest-scoring criterion
    lowest = min(evaluation["scores"], key=lambda k: evaluation["scores"][k])
    lowest_score = evaluation["scores"][lowest]

    print(f"""
The single weakest point:
  {lowest} — score {lowest_score}/5
  Note: {evaluation["notes"][lowest]}

Fix exactly this one thing. Do not change anything else.
""")

    change_description = input("What one change will you make to the prompt? ").strip()
    refined_prompt = prompt_input("Your refined prompt (v2):")

    return {
        "original_prompt": draft["prompt"],
        "change_made": change_description,
        "refined_prompt": refined_prompt,
        "version": 2,
    }


def stage_document(definition, draft, evaluation, refinement):
    """Stage 6: Create a structured record of the prompt."""
    stage_header(6, "DOCUMENT")
    print("""
Documenting this prompt creates a permanent asset in your Prompt Library.
Fill in the details below.
""")

    name = input("Give this prompt a name (e.g. 'Code Explainer v1'): ").strip()
    limitations = input("What does this prompt handle poorly? ").strip()
    best_for = input("What is it best used for? ").strip()

    record = {
        "name": name,
        "date": datetime.date.today().isoformat(),
        "day": 1,
        "domain": "AI & Automation",
        "task_definition": definition,
        "prompt_v1": draft["prompt"],
        "prompt_v2": refinement["refined_prompt"],
        "change_v1_to_v2": refinement["change_made"],
        "evaluation": {
            "scores": evaluation["scores"],
            "notes": evaluation["notes"],
            "average": evaluation["average"],
        },
        "limitations": limitations,
        "best_for": best_for,
    }

    return record


def stage_reuse(record):
    """Stage 7: Convert the documented prompt into a reusable template."""
    stage_header(7, "REUSE")
    print("""
Convert your best prompt into a template using [VARIABLE] notation.

Example:
  Original: "Explain what a neuron is to a 16-year-old student."
  Template: "Explain what [TOPIC] is to a [AUDIENCE] [LEVEL] student."

This template works for any topic, audience, and level.
""")

    template = prompt_input("Your template version of the prompt:")
    variables = input("List the variables you used (comma-separated): ").strip()
    variables_list = [v.strip() for v in variables.split(",")]

    record["template"] = {
        "prompt": template,
        "variables": variables_list,
    }

    return record


# ─────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────

def save_record(record):
    """Save the complete session record to a JSON file."""
    filename = f"day001_prompt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"\nRecord saved to: {filename}")
    return filename


def print_completion_record(record):
    """Print the Day 1 Completion Record."""
    header("DAY 1 COMPLETION RECORD")
    print(f"""
PROJECT:           Map: Prompt Engineering Workflow — Cycle 1
DOMAIN:            AI & Automation
DATE:              {record['date']}
DAY:               1 of 1825
TECHNOLOGIES:      Python 3, Markdown, HTML, CSS

WHAT WAS BUILT:    Seven-stage workflow map (Markdown), visual reference
                   page (HTML/CSS), prompt testing system (Python)

SKILLS DEVELOPED:  Prompt definition, component identification, systematic
                   evaluation, iterative refinement, template creation,
                   workflow documentation

PROMPT CREATED:    {record.get('name', 'Unnamed')}
EVALUATION AVG:    {record['evaluation']['average']}/5
TEMPLATE CREATED:  {'Yes' if 'template' in record else 'No'}

NEXT PROJECT:      Day 2 — {next_project_name()}
""")


def next_project_name():
    """Returns the Day 2 project name."""
    return "Explain: Python Utility — Cycle 1 (Programming & Software)"


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    os.system("clear" if os.name == "posix" else "cls")
    header("GRIT — DAY 1 OF 1825 | PROMPT ENGINEERING WORKFLOW TESTER")
    print("""
Welcome to Day 1.

This script guides you through the seven-stage Prompt Engineering
Workflow. At the end, it produces a structured record for your
Prompt Library and a Day 1 Completion Record.

The workflow: DEFINE → DRAFT → TEST → EVALUATE → REFINE → DOCUMENT → REUSE
""")
    input("Press Enter to begin Stage 1...")

    # Run all seven stages
    definition = stage_define()
    draft = stage_draft(definition)
    result = stage_test(draft)
    evaluation = stage_evaluate(definition, result)

    if evaluation["average"] < 2.5:
        print("\nScore too low to proceed to documentation.")
        print("Return to Stage 1 and redefine the task.")
        return

    refinement = stage_refine(draft, evaluation)
    record = stage_document(definition, draft, evaluation, refinement)
    record = stage_reuse(record)

    # Save and print
    filename = save_record(record)
    print_completion_record(record)

    header("WORKFLOW COMPLETE")
    print(f"""
You have completed Day 1 of 1825.

Files created today:
  workflow.md          — Seven-stage workflow reference
  index.html           — Visual reference page (open in any browser)
  prompt_tester.py     — This script
  {filename}  — Today's prompt record

Commit these to Git. You will return to this workflow on Day 13.

GRIT — Learn. Build. Teach.
""")


if __name__ == "__main__":
    main()
