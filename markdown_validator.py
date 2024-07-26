import os
import re
import unittest

# Load template file for md
def load_template_fields(template_path):
    with open(template_path, 'r') as file:
        content = file.read()

    # Regex to extract fields in template
    field_pattern = re.compile(r'^(\w+): .+', re.MULTILINE)
    required_fields = field_pattern.findall(content)

    return required_fields

class TestMarkdownValidation(unittest.TestCase):
    
    def setUp(self):
        self.template_path = 'posts/template.md.tmpl'
        self.directory = 'posts/en'
        self.required_fields = load_template_fields(self.template_path)

    def validate_markdown(self, file_path):
        firstNine = []
        with open(file_path, 'r') as file:
            # Save the first nine rows of the template (header)
            for i, line in enumerate(file):
                if i < 9:
                    firstNine.append(line.strip())
                else:
                    break
            content = file.read()

        for i, field in enumerate(self.required_fields):
            # Check if field is in the markdown file
            self.assertIn(field, firstNine[i], f'Field {field} not found in {file_path}')
            
            # Check for different patterns of particular fields 
            if field == 'author_image':
                pattern = r'^author_image:\s+[\w.-]+\.(jpg|jpeg|png|gif|bmp)$'
                self.assertRegex(firstNine[i], pattern, f'Field {field} does not match the pattern')
            elif field == 'date':
                pattern = r'^date:\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}$'
                self.assertRegex(firstNine[i], pattern, f'Field {field} does not match the pattern')
            elif field == 'image':
                pattern = r'^image:\s+[\w.-]+\.(jpg|jpeg|png|gif|bmp)$'
                self.assertRegex(firstNine[i], pattern, f'Field {field} does not match the pattern')
            
        # Check if the markdown file contains the '---' separator
        self.assertIn('---', content, f"The string '---' is not contained in {file_path}")

    def test_validate_all_markdown(self):
        for filename in os.listdir(self.directory):
            if filename.endswith('.md'):
                self.validate_markdown(os.path.join(self.directory, filename))

if __name__ == '__main__':
    unittest.main()
