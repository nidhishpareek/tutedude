file_name = "sample_output.txt"

with open(file_name, "w") as file:
    file.write("Hello, this is my first file write program.\n")
    file.write("Python file handling is simple and useful.\n")

print(f"Content written successfully to {file_name}")
