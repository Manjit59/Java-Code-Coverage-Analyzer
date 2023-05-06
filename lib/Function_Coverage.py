import tkinter as tk
from tkinter import filedialog, messagebox
import re


class FunctionCoverage:
    def __init__(self, master):
        self.master = master
        self.master.title("Function Coverage")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        self.file_path = tk.StringVar()
        self.functions = {}

        tk.Label(self.master, text="Enter Java file path:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.master, textvariable=self.file_path).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.master, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(self.master, text="Process", command=self.process_file).grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    """def browse_file(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("Java files", "*.java"), ("all files", "*.*")))
        if file_path:
            self.file_path.set(file_path)"""

    def process_file(file_path):
        #file_path = self.file_path.get()
        try:
            with open(file_path) as f:
                code = f.read()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
            return

        self.process_functions(code)
        self.process_calls(code)
        self.show_results()

    def process_functions(self, code):
        function_regex = r"(public|private|protected|static|\s) +[\w<>]+\s+(\w+) *\([^\)]*\) *(\{?)"
        matches = re.finditer(function_regex, code)
        for match in matches:
            modifiers = match.group(1)
            name = match.group(2)
            start = match.start()
            end = self.find_function_end(code, start)

            function_node = FunctionNode(name, modifiers, code[start:end])
            self.functions[name] = function_node

    def find_function_end(self, code, start):
        count = 1
        i = start + 1
        while count > 0 and i < len(code):
            if code[i] == "{":
                count += 1
            elif code[i] == "}":
                count -= 1
            i += 1
        return i

    def process_calls(self, code):
        call_regex = r"([\w\.]+)\("
        matches = re.finditer(call_regex, code)

        for match in matches:
            function_name = match.group(1)
            if function_name in self.functions:
                # Check if the match is a function call
                if self.is_function_call(code, match.start()):
                    function_start = match.start()
                    function_end = self.find_function_end(code, function_start)

                    call_context = self.find_call(code, function_start)
                    self.functions[function_name].add_call(call_context)
                    self.functions[function_name].call_count += 1

    def is_function_call(self, code, start):
        # Check if the match is preceded by an identifier or a dot
        # This ensures that it's a function call and not just a function name
        i = start - 1
        while i >= 0 and code[i].isspace():
            i -= 1
        if i >= 0 and (code[i].isidentifier() or code[i] == "."):
            return True
        return False


    def find_call(self, code, start):
        context = ""
        i = start - 1
        while i >= 0:
            if code[i] == ";":
                break
            elif code[i] == ")":
                context += ")"
                count = 1
                i -= 1
                while count > 0 and i >= 0:
                    if code[i] == ")":
                        count += 1
                    elif code[i] == "(":
                        count -= 1
                    i -= 1
            elif code[i] == "{":
                context += "code block"
            elif code[i] == "(":
                context += "function call"
            i -= 1
        return context
    def show_results(self):
        # Define box drawing characters
        horizontal = "─"
        vertical = "│"
        topLeft = "┌"
        topRight = "┐"
        bottomLeft = "└"
        bottomRight = "┘"
        topMiddle = "┬"
        bottomMiddle = "┴"
        middleLeft = "├"
        middleMiddle = "┼"
        middleRight = "┤"

        # Calculate the maximum width of the box
        max_width = max(len(name) + 12 for name in self.functions.keys())

        # Build the matrix
        matrix = [[None for _ in range(len(self.functions) + 1)] for _ in range(len(self.functions) + 2)]
        matrix[0][0] = f"{topLeft}{horizontal*max_width}{topMiddle}"
        matrix[0][-1] = f"{topRight}{horizontal*max_width}{topMiddle}"
        matrix[-1][0] = f"{bottomLeft}{horizontal*max_width}{bottomMiddle}"
        matrix[-1][-1] = f"{bottomRight}{horizontal*max_width}{bottomMiddle}"
        for i in range(1, len(matrix[0])-1):
            matrix[0][i] = f"{topMiddle}{horizontal*max_width}{topMiddle}"
        for i in range(1, len(matrix)-1):
            matrix[i][0] = f"{vertical}{'Function':^{max_width}}{vertical}"
            matrix[i][-1] = f"{vertical}{'Calls':^{max_width}}{vertical}"
        for i, function in enumerate(self.functions.values(), 1):
            matrix[i][0] = f"{vertical}{function.name:^{max_width}}{vertical}"
            matrix[i][-1] = f"{vertical}{function.call_count:^{max_width}}{vertical}"
            for j, called_function in enumerate(self.functions.values(), 1):
                if called_function.name in function.calls:
                    matrix[i][j] = f"{vertical}{'X':^{max_width}}{vertical}"
                else:
                    matrix[i][j] = f"{vertical}{' ':^{max_width}}{vertical}"

        # Display the matrix in the text widget
        result_text = ""
        for row in matrix:
            result_text += " ".join([str(item) if item is not None else "" for item in row]) + "\n"

        # Create a text widget to display the results
        root = tk.Tk()
        root.title("Function Coverage Results")
        root.geometry(f"{max_width*7}x400")
        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget = tk.Text(root, wrap="none", yscrollcommand=scrollbar.set, font=("Consolas", 12))
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        # Display the results in the text widget
        text_widget.insert(tk.END, result_text)
        text_widget.config(state=tk.DISABLED)

        
class FunctionNode:
    def __init__(self, name, modifiers, code):
        self.name = name
        self.modifiers = modifiers
        self.code = code
        self.calls = {}
        self.call_count = 0

    def add_call(self, context):
        if context in self.calls:
            self.calls[context] += 1
        else:
            self.calls[context] = 1


if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionCoverage(root)
    root.mainloop()
