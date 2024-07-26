import os
import re

# List of required fields in the markdown file
REQUIRED_FIELDS = [
    'title', 'subtitle', 'author', 'author_image',
    'date', 'image', 'permalink', 'tags', 'shortcontent'
]

def validate_markdown(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Check if each required field is present and correctly formatted
    for field in REQUIRED_FIELDS:
        if not re.search(f'^{field}: .+', content, re.MULTILINE):
            # print(f'Missing or incorrect {field} in {file_path}')
            return False
        
    # Check if the markdown file contains the '---' separator
    if '---' not in content:
        # print(f'Missing --- separator in {file_path}')
        return False

    # print(f'{file_path} is valid.')
    return True

def validate_all_markdown(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            validate_markdown(os.path.join(directory, filename))

if __name__ == '__main__':
    validate_all_markdown('posts/en')
