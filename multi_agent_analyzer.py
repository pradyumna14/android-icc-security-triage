import json
from google import genai

API_KEY = "API"

client = genai.Client(api_key=API_KEY)

with open("security_report.json", "r") as f:
    report = json.load(f)

results = []

for finding in report["icc_findings"]:

    print("\n" + "=" * 80)
    print("Analyzing:", finding["component"])
    print("=" * 80)

    finding_json = json.dumps(finding, indent=4)

    # --------------------------------------------------
    # AGENT 1: RISK AGENT
    # --------------------------------------------------

    risk_prompt = f"""
You are an Android security researcher.

Analyze the following Android component metadata.

Component:

{finding_json}

Your task:

1. Identify possible security risks.
2. Explain potential attack paths.
3. List attacker prerequisites.
4. Estimate potential impact.
5. Assign severity (Low/Medium/High).

Only use the provided data.
Clearly separate facts from assumptions.
"""

    risk_response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=risk_prompt
    )

    risk_analysis = risk_response.text

    print("\n[RISK AGENT]\n")
    print(risk_analysis)

    # --------------------------------------------------
    # AGENT 2: VERIFICATION AGENT
    # --------------------------------------------------

    verify_prompt = f"""
You are an Android security reviewer.

Review the following component and challenge the risk analysis.

Component:

{finding_json}

Risk Analysis:

{risk_analysis}

Your task:

1. Explain why exploitation may not work.
2. Identify Android protections.
3. Explain intended functionality.
4. Determine whether findings may be false positives.
5. Clearly distinguish facts from assumptions.

Only use evidence that can reasonably be inferred from Android behavior.
"""

    verify_response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=verify_prompt
    )

    verify_analysis = verify_response.text

    print("\n[VERIFICATION AGENT]\n")
    print(verify_analysis)

    # --------------------------------------------------
    # AGENT 3: FINAL JUDGE
    # --------------------------------------------------

    judge_prompt = f"""
You are the FINAL Android security reviewer.

Your job is NOT to agree with either agent.

Your job is to determine what can actually be supported by evidence.

Component:

{finding_json}

Risk Analysis:

{risk_analysis}

Verification Analysis:

{verify_analysis}

IMPORTANT RULES:

1. Never assume source code behavior.
2. Never assume validation exists unless shown.
3. Never assume validation does NOT exist unless shown.
4. Only use evidence present in:
   - Android manifest data
   - Component metadata
   - Intent actions
   - Intent categories
   - Exported status
   - Permissions
5. If a claim requires source code inspection, explicitly state that.
6. Be skeptical of both agents.
7. Distinguish facts from assumptions.

For every important claim provide an Evidence Level:

- HIGH = directly observed in provided data
- MEDIUM = reasonable Android inference
- LOW = assumption requiring code review

Output format:

Classification:
(Real Vulnerability / False Positive / Needs Manual Review)

Confidence:
(Low / Medium / High)

Observed Facts:
- Fact
- Fact

Risk Claims:
- Claim
- Evidence Level
- Supported by data? Yes/No

Verification Claims:
- Claim
- Evidence Level
- Supported by data? Yes/No

What Cannot Be Determined:
- Item
- Why

Final Justification:
Provide a concise security assessment based only on available evidence.
"""

    judge_response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=judge_prompt
    )

    print("\n[FINAL JUDGE]\n")
    print(judge_response.text)

    results.append({
        "component": finding["component"],
        "judge_output": judge_response.text
    })

with open("final_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("\nDone.")
print("Results saved to final_results.json")