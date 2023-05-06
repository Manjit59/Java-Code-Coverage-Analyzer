import re

def read_java_file(file_path):
    """
    Read the contents of a Java file and return them as a string.
    """
    with open(file_path, "r") as file:
        java_code = file.read()
    return java_code

def extract_conditional_statements(java_code):
    """
    Extract the conditional statements from a Java code string using a regular expression,
    and return them as a string.
    """
    conditional_regex = re.compile(r"(if\s*\(.+?\)\s*\{.+?\}(?:\s*else\s*\{.+?\})*)", re.DOTALL)
    conditional_statements = "\n".join(conditional_regex.findall(java_code))
    return conditional_statements

def save_conditional_statements(conditional_statements, file_path="Result\\ConResult.txt"):
    """
    Save the conditional statements string to a file.
    """
    with open(file_path, "w") as file:
        file.write(conditional_statements)
