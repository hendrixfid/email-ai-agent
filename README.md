**AI Email Triage Agent**



An AI-powered Python agent that automatically classifies and drafts replies 

for incoming business emails — built as a demo for AI automation roles.



**What It Does**

\- Reads a simulated business inbox

\- Classifies each email (Quote Request, Complaint, Billing Issue, etc.)

\- Assigns a priority level (High, Medium, Low)

\- Drafts a professional reply for each email

\- Outputs a clean HTML report



**Tech Stack**

\- Python

\- Groq API (LLaMA 3.3 70B)

\- HTML/CSS for report output



**How to Run**
1\. Clone the repository

2\. Create a virtual environment and activate it

3\. Install dependencies

4\. Add your Groq API key to a `.env` file

5\. Run the agent



**Setup**

```bash

python -m venv venv

venv\\Scripts\\activate

pip install groq python-dotenv

```



Run

```bash

python agent.py

```



Then open `report.html` in your browser to see the results.



**Sample Output:**<img width="1918" height="945" alt="Screenshot" src="https://github.com/user-attachments/assets/4727c38d-b782-400b-8a92-5a9626298480" />




