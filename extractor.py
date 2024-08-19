def extract_content(file_content):
    # Split the content into lines
    lines = file_content.splitlines()

    # Find the starting point where the header is located
    start_index = 0
    for i, line in enumerate(lines):
        if "Link Speed" in line:
            start_index = i
            break

    # Extract content starting from the header line
    extracted_content = "\n".join(lines[start_index:])

    return extracted_content

# Open the file and read its content
with open('status-172.27.99.170.log', 'r') as file:
    file_content = file.read()

# Call the function with the content from the file
result = extract_content(file_content)

result = result.replace("---- More ----", "")

with open("status-172.27.99.170.log", 'w') as file:
    # Write the new content to the file
    file.write(result)
