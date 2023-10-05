# To analyze the code more deeply, let's break it down into its individual functions and main execution block.
# This will help us identify specific areas that may need improvement or are causing issues.

# Split the script by lines
script_lines = original_script_content.split("\n")

# Variables to hold different code blocks
current_function = []
functions = {}
main_execution_block = []

# Flag to check if we are inside a function
inside_function = False

# Go through each line and separate them into functions and the main execution block
for line in script_lines:
    if line.startswith("def "):
        inside_function = True
        current_function = [line]
    elif inside_function and line.strip() == "":
        inside_function = False
        function_name = current_function[0].split("(")[0][4:]
        functions[function_name] = current_function
    elif inside_function:
        current_function.append(line)
    else:
        main_execution_block.append(line)

# Display function names and main execution block first few lines for an overview
list(functions.keys()), main_execution_block[:10]
