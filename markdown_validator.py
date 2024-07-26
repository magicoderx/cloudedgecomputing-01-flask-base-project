import os
import re

# Load template file for md
def load_template_fields(template_path):
    with open(template_path, 'r') as file:
        content = file.read()

    # Regex to extract fields in template
    field_pattern = re.compile(r'^(\w+): .+', re.MULTILINE)
    required_fields = field_pattern.findall(content)

    return required_fields

def validate_markdown(file_path, required_fields):
    firstNine=[]
    with open(file_path, 'r') as file:
        # Save the first nin rows of template (header)
        for i, riga in enumerate(file):
            if i < 9:
                firstNine.append(riga.strip())
            else:
                break
        content = file.read()

    for i,field in enumerate(required_fields):
        # Check if field is in the markdown file
        if not field in firstNine[i]:
            return False
        # Check for different patterns of particular fields 
        if field=='author_image':
            pattern = r'^author_image:\s+[\w.-]+\.(jpg|jpeg|png|gif|bmp)$'
            if not re.match(pattern,firstNine[i]):
                return False
        elif field=='date':
            pattern = r'^date:\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}$'
            if not re.match(pattern,firstNine[i]):
                return False
        elif field=='image':
            pattern = r'^image:\s+[\w.-]+\.(jpg|jpeg|png|gif|bmp)$'
            if not re.match(pattern,firstNine[i]):
                return False
        
    # Check if the markdown file contains the '---' separator
    if '---' not in content:
        return False

    return True

def validate_all_markdown(directory, template_path):
    required_fields = load_template_fields(template_path)
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            return validate_markdown(os.path.join(directory, filename), required_fields)

if __name__ == '__main__':
    template_path = 'posts/template.md.tmpl'
    directory = 'posts/en'
    validate_all_markdown(directory, template_path)

