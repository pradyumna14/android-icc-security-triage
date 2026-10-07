import json
from google import genai

# Put your Gemini API key here
API_KEY = "API"

client = genai.Client(api_key=API_KEY)

with open("security_report.json", "r") as f:
    report = json.load(f)

prompt = f"""
You are an expert Android security researcher specializing in
Android Inter-Component Communication (ICC) security analysis.

Your task is to analyze the findings and determine whether each
finding is:

- Real Vulnerability
- False Positive
- Needs Manual Review

IMPORTANT:

Use Android-specific context when reasoning:

- Exported status
- Permissions
- Intent actions
- Intent categories
- Android component purpose
- Expected Android platform behavior

Examples:

MAIN + LAUNCHER activity
→ Usually required by Android
→ Likely False Positive

Panic responder activity
→ May intentionally receive external intents
→ Evaluate intended functionality

For EACH finding provide:

Component:
Decision: (Real Vulnerability / False Positive / Needs Manual Review)
Severity: (Low / Medium / High)
Confidence: (Low / Medium / High)
Reasoning:

Finally provide:

Overall Assessment:
- How many findings are likely real vulnerabilities?
- How many are likely false positives?
- Would a security analyst need to investigate further?

Android ICC Report:

{json.dumps(report, indent=4)}
"""

print("Sending report to Gemini...")

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

print("\nResponse received!\n")
print(response.text)