from groq import Groq
import json
import time
import os
from dotenv import load_dotenv
from emails import emails

# ---- CONFIG ----
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

# ---- CORE FUNCTION ----
def process_email(email):
    prompt = f"""
You are an AI assistant for an Australian roofing and cladding construction company.

Analyze this email and respond in valid JSON only, no markdown, no explanation.

Email:
Sender: {email['sender']}
Subject: {email['subject']}
Body: {email['body']}

Return this exact JSON structure:
{{
  "category": "one of: Quote Request, Complaint, Partnership Inquiry, Billing Issue, Spam, General Inquiry",
  "priority": "one of: High, Medium, Low",
  "summary": "one sentence summary of the email",
  "suggested_reply": "a professional reply email from the company. If spam, write NONE."
}}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    text = response.choices[0].message.content.strip()

    # Clean up markdown fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    return json.loads(text.strip())

# ---- RUN AGENT ----
results = []
print("Processing emails...\n")

for email in emails:
    print(f"  → Analyzing: {email['subject']}")
    result = process_email(email)
    results.append({**email, **result})
    time.sleep(2)

# ---- GENERATE HTML REPORT ----
priority_colors = {"High": "#e74c3c", "Medium": "#f39c12", "Low": "#27ae60"}
category_icons = {
    "Quote Request": "💰", "Complaint": "😠", "Partnership Inquiry": "🤝",
    "Billing Issue": "🧾", "Spam": "🚫", "General Inquiry": "📩"
}

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Email Triage Report</title>
<style>
  body { font-family: Arial, sans-serif; background: #f0f2f5; padding: 30px; }
  h1 { color: #2c3e50; }
  .email-card { background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 5px solid #3498db; }
  .meta { display: flex; gap: 15px; margin-bottom: 10px; align-items: center; }
  .badge { padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; color: white; }
  .subject { font-size: 18px; font-weight: bold; color: #2c3e50; }
  .sender { color: #7f8c8d; font-size: 14px; margin-bottom: 8px; }
  .summary-box { background: #eaf4fb; border-radius: 6px; padding: 10px; margin: 10px 0; font-size: 14px; }
  .reply-box { background: #f9f9f9; border: 1px solid #ddd; border-radius: 6px;
               padding: 12px; font-size: 13px; white-space: pre-wrap; margin-top: 10px; }
  .reply-label { font-weight: bold; color: #555; margin-top: 12px; }
</style>
</head>
<body>
<h1>📬 AI Email Triage Report</h1>
<p style="color:#555">Processed by AI Email Agent &mdash; """ + str(len(results)) + """ emails analyzed</p>
"""

for r in results:
    color = priority_colors.get(r['priority'], '#3498db')
    icon = category_icons.get(r['category'], '📩')
    html += f"""
<div class="email-card" style="border-left-color:{color}">
  <div class="subject">{icon} {r['subject']}</div>
  <div class="sender">From: {r['sender']}</div>
  <div class="meta">
    <span class="badge" style="background:{color}">{r['priority']} Priority</span>
    <span class="badge" style="background:#8e44ad">{r['category']}</span>
  </div>
  <div class="summary-box">📝 <strong>Summary:</strong> {r['summary']}</div>
  <div class="reply-label">✉️ Suggested Reply:</div>
  <div class="reply-box">{r['suggested_reply']}</div>
</div>
"""

html += "</body></html>"

with open("report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\n✅ Done! Open report.html to see the results.")