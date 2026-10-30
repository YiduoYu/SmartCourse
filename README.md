# CPS3320-SmartCourse_AI_Course_Advisor

Final project for **CPS 3320 Python Programming** at Wenzhou-Kean University.

**SmartCourse** is a course management system for students and instructors with an AI advising module. A locally deployed LLM (`deepseek-r1:1.5b` via Ollama) reads a student's transcript and the major's study plan, then recommends the next courses to take.

## Features
- **Accounts**: registration restricted to `@kean.edu` addresses; instructors need a verification code
- **Students**: search the course catalog, enroll and drop courses, view grades
- **Instructors**: view course rosters and assign grades with validation
- **AI advising**: prompts built from the student's completed courses and the major plan (`cps_plan.txt`, `math_plan.txt`, `acct_plan.txt`), answered by a local model so no student data leaves the machine
- **Email notifications** for enrollment, drops, and grades
- **Three interfaces**: CLI (`main.py`), web UI with Gradio (`ui_gradio.py`), and desktop UI with PyQt (`ui_pyqt.py`)

## Running
```bash
cd SmartCourse
pip install gradio requests pyqt5

# AI advising (optional)
ollama pull deepseek-r1:1.5b && ollama serve

# Email notifications (optional)
export SMTP_USER="you@example.com"
export SMTP_PASSWORD="your-app-password"

python main.py         # CLI
python ui_gradio.py    # web UI at http://127.0.0.1:7860
python ui_pyqt.py      # desktop UI
```

## Data files
| File | Contents |
|---|---|
| `course_list.txt` | Course catalog |
| `account.txt` | User accounts (sample data) |
| `enrolled_courses.txt` | Enrollments and grades |
| `*_plan.txt` | Study plan for each major, used by the AI module |
| `log.txt` | Activity log |
