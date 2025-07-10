import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QLabel, QPushButton, QLineEdit, QRadioButton, QComboBox,
    QListWidget, QMessageBox, QDialog, QVBoxLayout, QHBoxLayout,
    QFormLayout, QInputDialog, QTextEdit
)
from PyQt5.QtGui import QFont, QCloseEvent, QTextOption # Used for custom close event handling
from PyQt5.QtCore import Qt # Used for alignment and other constants

# Import the course manager and utility functions
from course_manager import CourseManager
from utils import write_log, send_enrollment_email, send_grade_email, ask_ai_question

class SmartCourseUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartCourse")  # window title
        self.manager = CourseManager()      # course manager instance
        self.current_user = None
        self.current_is_student = None

        # Setup main window size and central widget
        self.resize(600, 400)

        # Create a stacked widget to hold different pages
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # Initialize all pages
        self._init_main_menu_page()
        self._init_login_page()
        self._init_register_page()
        self._init_student_menu_page()
        self._init_instructor_menu_page()

        # Set the initial page to main menu
        self.stack.setCurrentWidget(self.page_main_menu)

    def _init_main_menu_page(self):
        # Main menu page setup
        self.page_main_menu = QWidget()
        layout = QVBoxLayout(self.page_main_menu)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Display welcome title
        label_title = QLabel("Welcome to SmartCourse!")
        font_title = QFont()
        font_title.setPointSize(16)
        font_title.setBold(True)
        label_title.setFont(font_title)
        label_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_title)

        # Display main menu label
        label_menu = QLabel("Main Menu")
        font_menu = QFont()
        font_menu.setPointSize(12)
        label_menu.setFont(font_menu)
        label_menu.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_menu)

        # Create buttons for Login, Register, and Exit
        btn_login = QPushButton("Login")
        btn_register = QPushButton("Register")
        btn_exit = QPushButton("Exit")
        btn_login.setFixedWidth(120)
        btn_register.setFixedWidth(120)
        btn_exit.setFixedWidth(120)
        # Set button styles
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(btn_login)
        btn_layout.addWidget(btn_register)
        btn_layout.addWidget(btn_exit)
        btn_layout.setSpacing(15)
        layout.addLayout(btn_layout)

        # Connect buttons to their respective actions
        btn_login.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_login))
        btn_register.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_register))
        btn_exit.clicked.connect(self.exit_application)

        self.stack.addWidget(self.page_main_menu)
    # Resize event to adjust fonts and button sizes
    def resizeEvent(self, event):
        base_width = 600
        scale = self.width() / base_width
        self.update_fonts(self, scale)
        super().resizeEvent(event)

    # Update fonts and button sizes based on the current scale
    def update_fonts(self, widget, scale):
        for child in widget.findChildren(QWidget):
            if isinstance(child, (QLabel, QPushButton, QLineEdit)):
                font = child.font()
                font_size = max(10, min(int(12 * scale), 24))
                title_size = max(14, min(int(16 * scale), 32))
                font.setPointSize(title_size if "Menu" in child.text() or "Welcome" in child.text() else font_size)
                child.setFont(font)

                # Automatically adjust button sizes
                if isinstance(child, QPushButton):
                    child.setMinimumHeight(int(40 * scale))
                    child.setMinimumWidth(int(160 * scale))
                elif isinstance(child, QLineEdit):
                    child.setMinimumHeight(int(30 * scale))

            self.update_fonts(child, scale)
    # Show scaled dialog with updated fonts
    def show_scaled_dialog(self, dialog: QDialog):
        scale = self.width() / 600
        self.update_fonts(dialog, scale)
        dialog.exec_()

    def show_scaled_message(self, title: str, icon: QMessageBox.Icon = QMessageBox.Information):
        # Show a message box with scaled fonts
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setIcon(icon)
        msg_box.setText(title)
        self.update_fonts(msg_box, self.width() / 600)
        msg_box.exec_()

    def _init_login_page(self):
        # Initialize the login page
        self.page_login = QWidget()
        layout = QVBoxLayout(self.page_login)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Display login title
        label = QLabel("Login")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Layout for username and password input
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(15)
        # Username input
        self.login_username_input = QLineEdit()
        self.login_username_input.setPlaceholderText("Enter your email (@kean.edu)")
        form_layout.addRow("Username:", self.login_username_input)
        # Password input
        self.login_password_input = QLineEdit()
        self.login_password_input.setEchoMode(QLineEdit.Password)
        self.login_password_input.setPlaceholderText("Enter your password")
        form_layout.addRow("Password:", self.login_password_input)
        layout.addLayout(form_layout)

        # Error label for login feedback(hide by default)
        self.login_error_label = QLabel("")
        self.login_error_label.setAlignment(Qt.AlignCenter)
        error_font = QFont()
        error_font.setPointSize(10)
        self.login_error_label.setFont(error_font)
        self.login_error_label.setStyleSheet("color: red;")
        self.login_error_label.hide()
        layout.addWidget(self.login_error_label)

        # Layout for login and cancel buttons
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignCenter)
        btn_login = QPushButton("Login")
        btn_cancel = QPushButton("Cancel")
        btn_login.setFixedWidth(100)
        btn_cancel.setFixedWidth(100)
        btn_row.addWidget(btn_login)
        btn_row.addWidget(btn_cancel)
        btn_row.setSpacing(20)
        layout.addLayout(btn_row)

        # Connect button events
        btn_login.clicked.connect(self.handle_login)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_main_menu))

        self.stack.addWidget(self.page_login)

    def _init_register_page(self):
        # Initialize the registration page
        self.page_register = QWidget()
        layout = QVBoxLayout(self.page_register)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(15)

        label = QLabel("Register New Account")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Form layout for registration inputs
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(10)
        # Username input
        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText("Email must end with @kean.edu")
        form_layout.addRow("New username:", self.reg_username_input)
        # Password input
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.reg_password_input)
        # Role choice (radio buttons)
        role_layout = QHBoxLayout()
        self.radio_student = QRadioButton("Student")
        self.radio_instructor = QRadioButton("Instructor")
        self.radio_student.setChecked(True)
        role_layout.addWidget(self.radio_student)
        role_layout.addWidget(self.radio_instructor)
        form_layout.addRow("Role:", role_layout)
        # Major selection (for students)
        self.reg_major_combo = QComboBox()
        self.reg_major_combo.addItems(["cps", "acct", "math"])
        form_layout.addRow("Major:", self.reg_major_combo)
        # Security code input (for instructors)
        self.reg_security_input = QLineEdit()
        self.reg_security_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Security code:", self.reg_security_input)

        layout.addLayout(form_layout)

        # Hide major and security input by default
        self.reg_security_input.hide()
        # When the page is shown, only show major for students
        self.radio_student.toggled.connect(self.on_role_toggle)

        # Error label for registration feedback (hide by default)
        self.reg_error_label = QLabel("")
        self.reg_error_label.setAlignment(Qt.AlignCenter)
        error_font = QFont()
        error_font.setPointSize(10)
        self.reg_error_label.setFont(error_font)
        self.reg_error_label.setStyleSheet("color: red;")
        self.reg_error_label.hide()
        layout.addWidget(self.reg_error_label)

        # Button row for register and cancel
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignCenter)
        btn_register = QPushButton("Register")
        btn_cancel = QPushButton("Cancel")
        btn_register.setFixedWidth(100)
        btn_cancel.setFixedWidth(100)
        btn_row.addWidget(btn_register)
        btn_row.addWidget(btn_cancel)
        btn_row.setSpacing(20)
        layout.addLayout(btn_row)

        # Connect button events
        btn_register.clicked.connect(self.handle_register)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_main_menu))

        self.stack.addWidget(self.page_register)

    def _init_student_menu_page(self):
        # Student main menu page setup
        self.page_student_menu = QWidget()
        layout = QVBoxLayout(self.page_student_menu)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        # Student menu title
        self.student_menu_label = QLabel("Student Menu")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.student_menu_label.setFont(font)
        self.student_menu_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.student_menu_label)

        # Welcome user label
        self.student_welcome_label = QLabel("")  # Like "Welcome, user@kean.edu!"
        self.student_welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.student_welcome_label)

        # Button list for student actions
        btn_enroll = QPushButton("Enroll in Course")
        btn_view_courses = QPushButton("View My Courses")
        btn_drop = QPushButton("Drop Course")
        btn_ask_ai = QPushButton("Ask AI for Advice")
        btn_exit = QPushButton("Exit")
        # Set fixed width for buttons
        for btn in (btn_enroll, btn_view_courses, btn_drop, btn_ask_ai, btn_exit):
            btn.setFixedWidth(180)
        # Button layout
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(10)
        btn_layout.addWidget(btn_enroll)
        btn_layout.addWidget(btn_view_courses)
        btn_layout.addWidget(btn_drop)
        btn_layout.addWidget(btn_ask_ai)
        # Keep some space before exit button
        btn_layout.addSpacing(5)
        btn_layout.addWidget(btn_exit)
        layout.addLayout(btn_layout)

        # Connect button events
        btn_enroll.clicked.connect(self.handle_enroll_course)
        btn_view_courses.clicked.connect(self.handle_view_my_courses)
        btn_drop.clicked.connect(self.handle_drop_course)
        btn_ask_ai.clicked.connect(self.handle_ask_ai)
        btn_exit.clicked.connect(self.handle_logout)  # Student logout

        self.stack.addWidget(self.page_student_menu)

    def _init_instructor_menu_page(self):
        # Instructor main menu page setup
        self.page_instructor_menu = QWidget()
        layout = QVBoxLayout(self.page_instructor_menu)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        # Instructor menu title
        self.instr_menu_label = QLabel("Instructor Menu")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.instr_menu_label.setFont(font)
        self.instr_menu_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instr_menu_label)

        # Welcome user label
        self.instr_welcome_label = QLabel("")
        self.instr_welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instr_welcome_label)

        # Button list for instructor actions
        btn_view_students = QPushButton("View Student Courses")
        btn_assign_grade = QPushButton("Assign Grade")
        btn_exit = QPushButton("Exit")
        btn_view_students.setFixedWidth(200)
        btn_assign_grade.setFixedWidth(200)
        btn_exit.setFixedWidth(200)
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(10)
        btn_layout.addWidget(btn_view_students)
        btn_layout.addWidget(btn_assign_grade)
        btn_layout.addSpacing(5)
        btn_layout.addWidget(btn_exit)
        layout.addLayout(btn_layout)

        # Connect button events
        btn_view_students.clicked.connect(self.handle_view_student_courses)
        btn_assign_grade.clicked.connect(self.handle_assign_grade)
        btn_exit.clicked.connect(self.handle_logout)  # Instructor logout

        self.stack.addWidget(self.page_instructor_menu)

    def on_role_toggle(self):
        if self.radio_student.isChecked():
            # Student: Display major, hide security
            self.reg_major_combo.show()
            self.reg_security_input.hide()
        else:
            # Instructor: Hide major, display security
            self.reg_major_combo.hide()
            self.reg_security_input.show()
        # Clear any previous error messages
        self.reg_error_label.hide()
        self.reg_error_label.setText("")

    def handle_login(self):
        # Handle login logic
        username = self.login_username_input.text().strip()
        password = self.login_password_input.text()
        # Authentication error label (hide by default)
        if not username.endswith("@kean.edu"):
            self.login_error_label.setText("Invalid username. Username must end with '@kean.edu'.")
            self.login_error_label.show()
            return
        # Check if the username is a student or instructor
        is_student = self.manager.is_student_account(username)
        if self.manager.authenticate_user(username, password, is_student):
            # Login successful
            write_log(f"{username} logged in")  # Record login event
            self.current_user = username
            self.current_is_student = is_student

            if is_student:
                self.student_menu_label.setText(f"Student Menu")
                self.student_welcome_label.setText(f"Welcome, {username}!")
                self.stack.setCurrentWidget(self.page_student_menu)
            else:
                self.instr_menu_label.setText(f"Instructor Menu")
                self.instr_welcome_label.setText(f"Welcome, {username}!")
                self.stack.setCurrentWidget(self.page_instructor_menu)
            # Clear input fields and hide error label
            self.login_username_input.clear()
            self.login_password_input.clear()
            self.login_error_label.hide()
        else:
            # Login failed
            self.login_error_label.setText("Login failed. Try again.")
            self.login_error_label.show()
            # Keep input fields for retry
            self.login_password_input.clear()

    def handle_register(self):
        # Handle registration logic
        username = self.reg_username_input.text().strip()
        password = self.reg_password_input.text()
        is_student = self.radio_student.isChecked()
        role_text = "student" if is_student else "instructor"

        # Clear any previous error messages
        self.reg_error_label.hide()
        self.reg_error_label.setText("")

        # Authentication checks
        if not username.endswith("@kean.edu"):
            self.reg_error_label.setText("Invalid username. Username must end with '@kean.edu'.")
            self.reg_error_label.show()
            return

        # Check if password is empty
        if not is_student:
            security_input = self.reg_security_input.text()
            from main import SECURITY_PASSWORD  # Get security password from main module
            if security_input != SECURITY_PASSWORD:
                self.reg_error_label.setText("Security password incorrect. Instructor account not created.")
                self.reg_error_label.show()
                return

        # Check if username already exists
        exists = False
        if self.manager.get_student_by_username(username) is not None:
            exists = True
        else:
            # Check instructors
            for instr in self.manager.instructors:
                if instr.username == username:
                    exists = True
                    break
        if exists:
            self.reg_error_label.setText("Username already exists. Please choose a different username.")
            self.reg_error_label.show()
            return

        # If student, check major
        major = None
        if is_student:
            major = self.reg_major_combo.currentText().strip().lower()
            if major not in ["cps", "acct", "math"]:
                self.reg_error_label.setText("Sorry, this system only supports cps, acct, and math majors.")
                self.reg_error_label.show()
                return

        # Create the account
        if is_student:
            # Add student object
            self.manager.students.append(__import__('data_models').Student(username, password, major))
        else:
            # Add instructor object
            self.manager.instructors.append(__import__('data_models').Instructor(username, password))
        # Save the new account
        self.manager.create_account(username, password, is_student)
        write_log(f"Created new account: {username}")  # Record account creation event

        # Show success message
        QMessageBox.information(self, "Success", "Account created. Please log in.")
        # Clear input fields
        self.reg_username_input.clear()
        self.reg_password_input.clear()
        self.reg_security_input.clear()
        # Reset role to student by default
        self.radio_student.setChecked(True)
        self.on_role_toggle()
        # Switch back to main menu
        self.stack.setCurrentWidget(self.page_main_menu)

    def handle_enroll_course(self):
        # Handle course enrollment
        # Create a dialog for course enrollment
        dialog = QDialog(self)
        dialog.setWindowTitle("Enroll in Course")
        dialog.setModal(True)
        dialog.resize(400, 300)
        vlayout = QVBoxLayout(dialog)
        vlayout.setContentsMargins(20, 20, 20, 20)
        vlayout.setSpacing(10)
        # Add label for instructions
        label = QLabel("Search and select a course to enroll:")
        vlayout.addWidget(label)
        # Search layout
        search_layout = QHBoxLayout()
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("Enter keyword (leave empty to show all)")
        search_btn = QPushButton("Search")
        search_layout.addWidget(search_edit)
        search_layout.addWidget(search_btn)
        vlayout.addLayout(search_layout)
        # Course list widget
        list_widget = QListWidget()
        vlayout.addWidget(list_widget)
        # Populate list with all courses initially
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        enroll_btn = QPushButton("Enroll")
        cancel_btn = QPushButton("Cancel")
        enroll_btn.setFixedWidth(100)
        cancel_btn.setFixedWidth(100)
        btn_layout.addWidget(enroll_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.setSpacing(20)
        vlayout.addLayout(btn_layout)

        # Define search behavior
        def do_search():
            keyword = search_edit.text().strip()
            # Search courses by keyword
            matched = self.manager.search_courses(keyword)
            list_widget.clear()
            if not matched:
                # No matching courses found
                QMessageBox.information(dialog, "No Results", "No matching courses found.")
                # Optionally, you can list all courses if keyword is empty
            else:
                # List matching courses
                for course in matched:
                    list_widget.addItem(course)
        search_btn.clicked.connect(do_search)

        # Define enrollment behavior
        def do_enroll():
            item = list_widget.currentItem()
            if item is None:
                QMessageBox.warning(dialog, "Enroll Course", "Please select a course to enroll.")
                return
            course_name = item.text()
            # Authenticate current user
            if course_name not in self.manager.courses:
                QMessageBox.warning(dialog, "Enroll Course", "Invalid course selection.")
                dialog.reject()  # Close dialog without enrolling
                return
            # Check if user is already enrolled in this course
            existing = self.manager.get_student_courses(self.current_user)
            if course_name in existing:
                QMessageBox.warning(dialog, "Enroll Course", "You are already enrolled in this course.")
                dialog.reject()
                return
            # Execute enrollment
            self.manager.enroll_student(self.current_user, course_name)
            write_log(f"{self.current_user} enrolled in {course_name}")
            # Send enrollment confirmation email
            send_enrollment_email(self.current_user,
                f"Dear {self.current_user}, \n\n"
                f"Congratulations! You have successfully enrolled in the course: {course_name}. \n"
                f"Please log into your account to review the course details and ensure it aligns with your academic goals.\n\n"
                f"Sincerely,\nKean University")

            QMessageBox.information(dialog, "Enroll Course", f"Successfully enrolled in {course_name}.")
            dialog.accept()
        enroll_btn.clicked.connect(do_enroll)
        cancel_btn.clicked.connect(dialog.reject)

        # Populate the course list with all courses initially
        self.show_scaled_dialog(dialog)


    def handle_view_my_courses(self):
        # Handle viewing enrolled courses
        courses = self.manager.get_student_courses(self.current_user)
        if not courses:
            QMessageBox.information(self, "My Courses", "You are not enrolled in any courses.")
        else:
            # Create a dialog to display courses
            course_lines = []
            for course_name, grade in courses.items():
                grade_text = grade if grade is not None else "Not assigned"
                course_lines.append(f"{course_name} - Grade: {grade_text}")
            courses_str = "\n".join(course_lines)
            QMessageBox.information(self, "My Courses",
                                    f"Courses enrolled by {self.current_user}:\n{courses_str}")

    def handle_drop_course(self):
        # Handle course dropping
        courses = self.manager.get_student_courses(self.current_user)
        if not courses:
            QMessageBox.information(self, "Drop Course", "You have no courses to drop.")
            return
        # Create a dialog for dropping courses
        dialog = QDialog(self)
        dialog.setWindowTitle("Drop Course")
        dialog.setModal(True)
        dialog.resize(400, 250)
        vlayout = QVBoxLayout(dialog)
        vlayout.setContentsMargins(20, 20, 20, 20)
        vlayout.setSpacing(10)
        label = QLabel("Select a course to drop:")
        vlayout.addWidget(label)
        list_widget = QListWidget()
        # List all courses the student is enrolled in
        for course_name in courses.keys():
            list_widget.addItem(course_name)
        vlayout.addWidget(list_widget)
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        drop_btn = QPushButton("Drop")
        cancel_btn = QPushButton("Cancel")
        drop_btn.setFixedWidth(100)
        cancel_btn.setFixedWidth(100)
        btn_layout.addWidget(drop_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.setSpacing(20)
        vlayout.addLayout(btn_layout)

        # Define the drop behavior
        def do_drop():
            item = list_widget.currentItem()
            if item is None:
                QMessageBox.warning(dialog, "Drop Course", "Please select a course to drop.")
                return
            course_name = item.text()
            # Check if the course is graded
            if courses.get(course_name) is not None:
                QMessageBox.warning(dialog, "Drop Course", "You cannot drop a course that has been graded.")
                dialog.reject()
                return
            # Execute the drop
            self.manager.drop_student_course(self.current_user, course_name)
            write_log(f"{self.current_user} dropped {course_name}")
            # Send drop confirmation email
            send_enrollment_email(self.current_user,
                  f"Dear {self.current_user}, \n\n"
                  f"You have successfully dropped the course: {course_name}. \n"
                  f"If this was a mistake, please log into your account to re-enroll in the course.\n\n"
                  f"Sincerely,\nKean University")
            QMessageBox.information(dialog, "Drop Course", "Course dropped.")
            dialog.accept()
        drop_btn.clicked.connect(do_drop)
        cancel_btn.clicked.connect(dialog.reject)

        self.show_scaled_dialog(dialog)

        # Go back to student menu after dialog closes
    def handle_ask_ai(self):
        # Handle AI question dialog
        # Create a dialog for asking AI questions
        dialog = QDialog(self)
        dialog.setWindowTitle("Ask AI for Advice")
        dialog.setModal(True)
        dialog.resize(500, 400)
        vlayout = QVBoxLayout(dialog)
        vlayout.setContentsMargins(20, 20, 20, 20)
        vlayout.setSpacing(10)
        label = QLabel("Enter your academic question:")
        vlayout.addWidget(label)
        question_edit = QLineEdit()
        question_edit.setPlaceholderText("E.g., What course should I take next?")
        vlayout.addWidget(question_edit)
        # Read-only text box
        from PyQt5.QtWidgets import QTextEdit
        answer_box = QTextEdit()
        answer_box.setReadOnly(True)
        answer_box.setWordWrapMode(QTextOption.WordWrap)
        answer_box.setVisible(False)  # Initially hidden
        answer_box.setMinimumHeight(200)
        vlayout.addWidget(answer_box)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        ask_btn = QPushButton("Ask")
        close_btn = QPushButton("Close")
        ask_btn.setFixedWidth(100)
        close_btn.setFixedWidth(100)
        btn_layout.addWidget(ask_btn)
        btn_layout.addWidget(close_btn)
        btn_layout.setSpacing(20)
        vlayout.addLayout(btn_layout)

        def do_ask():
            question = question_edit.text().strip()
            if not question:
                QMessageBox.warning(dialog, "Ask AI", "Please enter a question.")
                return
            # Get the student's course history
            student_courses = self.manager.get_student_courses(self.current_user)
            course_info_lines = [
                f"{course} - {grade if grade else 'Not assigned'}"
                for course, grade in student_courses.items()
            ]
            course_info = "\n".join(course_info_lines)
            plan_text = ""
            # Get the student's major and corresponding four-year plan
            student_obj = self.manager.get_student_by_username(self.current_user)
            major = student_obj.major if student_obj else None
            if major:
                try:
                    with open(f"{major}_plan.txt", "r", encoding="utf-8") as f:
                        plan_text = f.read()
                except FileNotFoundError:
                    plan_text = ""
            # Create the full prompt for AI
            full_prompt = (
                f'I am a student asking the following academic question:\n"{question}"\n'
                f"My current course history:\n{course_info}\n"
                f"Here is the four-year plan for my major:\n{plan_text}\n"
                f"Based on my question, my course history, and the plan above, give me a suggestion."
            )
            # Call the AI function to get an answer
            answer = ask_ai_question(full_prompt)

            answer_box.setPlainText(f"[AI ADVICE]\n{answer.strip()}")
            answer_box.setVisible(True)  # Show the answer box

            ask_btn.setEnabled(False)
        ask_btn.clicked.connect(do_ask)
        close_btn.clicked.connect(dialog.accept)

        self.show_scaled_dialog(dialog)

        # After the dialog closes, return to the student menu

    def handle_view_student_courses(self):
        # Handle viewing courses for a selected student
        # Get all students
        students = self.manager.list_all_students()
        if not students:
            QMessageBox.information(self, "View Student Courses", "No student accounts found.")
            return
        # Create a dialog to select a student
        student, ok = QInputDialog.getItem(self, "View Student Courses",
                                          "Select a student to view courses:",
                                          students, 0, False)
        if not ok or not student:
            return  # If user cancels, just return to menu
        # Get the courses for the selected student
        courses = self.manager.get_student_courses(student)
        if not courses:
            QMessageBox.information(self, "View Student Courses",
                                    f"No courses found for {student}.")
        else:
            course_lines = []
            for course_name, grade in courses.items():
                grade_text = grade if grade else "Not assigned"
                course_lines.append(f"{course_name} - Grade: {grade_text}")
            courses_str = "\n".join(course_lines)
            QMessageBox.information(self, "View Student Courses",
                                    f"Courses enrolled by {student}:\n{courses_str}")

    def handle_assign_grade(self):
        # Handle assigning grades to students
        # Get all students
        students = self.manager.list_all_students()
        if not students:
            QMessageBox.information(self, "Assign Grade", "No student accounts found.")
            return
        # Create a dialog to select a student
        student, ok = QInputDialog.getItem(self, "Assign Grade",
                                          "Select a student:", students, 0, False)
        if not ok or not student:
            return
        # Get the courses for the selected student
        courses = self.manager.get_student_courses(student)
        if not courses or len(courses) == 0:
            QMessageBox.information(self, "Assign Grade", f"No courses found for {student}.")
            return
        # Create a dialog to select a course
        course_names = list(courses.keys())
        course, ok = QInputDialog.getItem(self, "Assign Grade",
                                         f"Select a course of {student}:", course_names, 0, False)
        if not ok or not course:
            return
        # Check if the student is enrolled in the selected course
        if course not in courses:
            QMessageBox.warning(self, "Assign Grade", "Student is not enrolled in this course.")
            return
        # Create a dialog to select a grade
        grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"]
        grade, ok = QInputDialog.getItem(self, "Assign Grade",
                                        "Select a grade:", grades, 0, False)
        if not ok or not grade:
            return
        # Assign the grade to the student for the selected course
        self.manager.set_student_grade(student, course, grade)
        write_log(f"Assigned grade {grade} to {student} for {course}")
        # Send grade assignment confirmation email
        send_grade_email(student,
            f"Dear {student}, \n\n"
            f"You received grade '{grade}' for course {course}. \n"
            f"Please log into your account to review your grade and ensure it is correct.\n\n"
            f"Sincerely,\nKean University")
        QMessageBox.information(self, "Assign Grade",
                                f"Grade {grade} assigned to {student} for {course}.")
        # Return to instructor menu after assigning grade

    def handle_logout(self):
        # Handle user logout
        # Save current enrollments before logging out
        self.manager.save_enrollments()
        # Show goodbye message
        QMessageBox.information(self, "Goodbye", "Goodbye!")
        # Reset current user and role
        self.close()

    def exit_application(self):
        # Handle application exit
        # Save all enrollments before exiting
        self.manager.save_enrollments()
        self.close()

    def closeEvent(self, event: QCloseEvent):
        # Handle window close event
        try:
            self.manager.save_enrollments()
        except Exception as e:
            print(f"Error saving enrollments: {e}")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartCourseUI()
    window.show()
    sys.exit(app.exec_())
