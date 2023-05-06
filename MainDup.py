import os
import sys
from src.Java_CFG_IO_Count import *
from src.Condition_Coverage import *
from src.Function_Coverage import *
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog


class JavaAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Java Code Analyzer')
        self.setGeometry(100, 100, 800, 600)

        # Set up the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Set up the layouts
        main_layout = QHBoxLayout(central_widget)
        java_code_layout = QVBoxLayout()
        result_layout = QVBoxLayout()

        # Set up the Java code display area
        self.java_code = QPlainTextEdit()
        java_code_layout.addWidget(self.java_code)

        # Set up the buttons for selecting and analyzing the Java code
        select_button = QPushButton('Select Java file')
        select_button.clicked.connect(self.select_java_file)
        java_code_layout.addWidget(select_button)

        run_cfg_button = QPushButton('Generate CFG')
        run_cfg_button.clicked.connect(self.run_cfg_generation)
        java_code_layout.addWidget(run_cfg_button)

        run_pdf_button = QPushButton('Clear')
        run_pdf_button.clicked.connect(self.run_pdf_opening)
        java_code_layout.addWidget(run_pdf_button)

        # Add the Java code layout to the main layout
        main_layout.addLayout(java_code_layout)

        # Set up the results display area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        result_layout.addWidget(self.output_text)

        run_condition_button = QPushButton('Condition Coverage')
        run_condition_button.clicked.connect(self.run_condition_coverage)
        result_layout.addWidget(run_condition_button)

        run_function_button = QPushButton('Function Coverage')
        run_function_button.clicked.connect(self.run_function_coverage)
        result_layout.addWidget(run_function_button)

        run_test_button = QPushButton('Run Test Case for Condition Coverage')
        run_test_button.clicked.connect(self.run_test_case)
        result_layout.addWidget(run_test_button)

        run_path_button = QPushButton('Path Coverage(FUTURE WORK)')
        run_path_button.clicked.connect(self.run_path_coverage)
        result_layout.addWidget(run_path_button)

        # Add the results layout to the main layout
        main_layout.addLayout(result_layout)

        # Initialize the selected Java file path to None
        self.java_file_path = None

    def select_java_file(self):
        # Open a file dialog to select a Java file
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('Java files (*.java)')
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_() == QFileDialog.Accepted:
            self.java_file_path = file_dialog.selectedFiles()[0]

            # Read the Java code from the selected file and display it in the Java code display area
            with open(self.java_file_path, 'r') as f:
                self.java_code.setPlainText(f.read())

    def run_cfg_generation(self):
        create_control_flow_graph(self.java_file_path)
        self.output_text.setPlainText('CFG Generated')
        path='Result\\Control_Flow_Graph.pdf'
        subprocess.Popen([path], shell=True)

    def run_pdf_opening(self):
        self.output_text.setPlainText('Working on it')
        
    def run_condition_coverage(self):
        java_code=read_java_file(self.java_file_path)
        conditional_statements = extract_conditional_statements(java_code)
        save_conditional_statements(conditional_statements)
        path='Result\\ConResult.txt'
        with open(path, 'r') as f:
                self.output_text.setPlainText(f.read())
        

    def run_function_coverage(self):
        FunctionCoverage.process_file(self.java_file_path)
        self.output_text.setPlainText('Generating.')
        self.output_text.setPlainText('Generating..')
        self.output_text.setPlainText('Generating...')
        

    def run_test_case(self):
        if self.java_file_path:
            result = subprocess.run(['python', 'test_case.py', self.java_file_path], capture_output=True)
            self.output_text.setPlainText(result.stdout.decode())
        else:
            self.output_text.setPlainText('Please select a Java file first.')

    def run_path_coverage(self):
        if self.java_file_path:
            result = subprocess.run(['python', 'path_coverage.py', self.java_file_path], capture_output=True)
            self.output_text.setPlainText(result.stdout.decode())
        else:
            self.output_text.setPlainText('Please select a Java file first.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JavaAnalyzer()
    window.show()
    sys.exit(app.exec_())
