# CPS3320_FinalProject —— **SmartCourse: Course Selection System with AI Suggestion Module**

## **Introduction**

**SmartCourse** is an intelligent university course management system that simplifies course selection and academic planning for both students and instructors. The system allows students to register accounts, browse and enroll in courses, view current grades, and drop ungraded courses. Instructors can manage enrollments and assign grades. A key highlight is the integrated **AI suggestion module**, which provides personalized course recommendations based on students’ academic history and major-specific requirements.

---

## **Key Features**

### **1. Account Management and Authentication**

* **Email Validation**

  * Only official university email addresses (`@kean.edu`) are accepted during registration.
  * Instructor registration requires a security code for verification.

* **Secure Login**

  * Credentials are authenticated against stored user data.
  * Email domain checks are enforced at login.

---

### **2. Student Functions**

* **Course Search & Enrollment**

  * Keyword-based search through the course catalog.
  * Duplicate enrollment is automatically prevented.
  * Students receive email confirmations upon successful enrollment.

* **View Enrolled Courses & Grades**

  * Displays all enrolled courses.
  * Grades are shown if assigned; otherwise marked as "Not Assigned."

* **Drop Courses**

  * Only ungraded courses can be dropped.
  * Enrollment records are updated, and confirmation emails are sent automatically.

* **AI Academic Advice**

  * Based on major-specific study plans and past academic history.
  * Leverages a local AI model to recommend appropriate next-step courses.

---

### **3. Instructor Functions**

* **View Student Enrollments**

  * Access a list of enrolled students for each course.
  * View individual students' course selections and grade status.

* **Assign Grades**

  * Grades validated against predefined grading rules.
  * Students receive email notifications when grades are submitted.

---

### **4. Email Notification System**

* Automated alerts for:

  * Course enrollment
  * Course drop
  * Grade assignment
* Email service is customizable via SMTP settings in the configuration.

---

### **5. Dual Interface Options**

* **Command-Line Interface (CLI)**

  * Lightweight and fast.
  * Ideal for remote or terminal-based operations.

* **Graphical User Interface (GUI) with Gradio**

  * Intuitive web interface using form fields, buttons, and dropdown menus.
  * Easily accessible via local browser.

---

## **Installation and Setup**

### **Prerequisites**

* Python 3.8+
* Install required packages:

  ```bash
  pip install gradio requests
  ```

### **Project Files**

Ensure the following files are located in the project root directory:

* `course_list.txt` – Contains all available courses.
* `account.txt` – Stores user credentials (auto-created upon registration).
* `enrolled_courses.txt` – Tracks student enrollments and grades.
* *(Optional)* Major-specific curriculum files (e.g., `cps_plan.txt`) for AI suggestions.

---

## **Running the Application**

### **CLI Mode**

```bash
python main.py
```

* Register or log in via numeric options.
* Navigate through course management menus using terminal input.

### **Gradio GUI Mode**

```bash
python ui_gradio.py
```

* Open the URL displayed in the terminal (e.g., `http://127.0.0.1:7860/`).
* Access full functionality via an interactive web-based interface.

---

## **AI Suggestion Module Setup**

* Requires [Ollama](https://ollama.com/) to be installed locally.
* AI model used: `deepseek-r1:1.5b`
* Make sure the Ollama service is running on the default port (`11434`).
* SmartCourse sends anonymized academic data to the AI for generating personalized course suggestions.
* If the AI service is unavailable, error messages are displayed in the interface.

---

## **Conclusion**

**SmartCourse** delivers a seamless, secure, and AI-powered platform for academic planning and course management. It enhances student decision-making with intelligent recommendations and simplifies administrative tasks for instructors. Through its dual-interface support and integrated email notification system, SmartCourse provides a robust and user-friendly experience for modern university environments.


