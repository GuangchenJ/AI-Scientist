import re
import os
import charset_normalizer

def insert_references(template_path, reference_path, output_path=None):
    with open(template_path, 'r') as file:
        template_content = file.read()
    with open(reference_path, 'r') as file:
        reference_content = file.read()
    
    if "REFERENCES HERE" in template_content:
        new_content = template_content.replace(r'REFERENCES HERE', reference_content)
    else:
        # ensure that the backslashes in reference_content are properly escaped.
        reference_content = reference_content.replace('\\', '\\\\')
        pattern = r'\\begin{filecontents}{references\.bib}(.*?)\\end{filecontents}'
        new_content = re.sub(pattern, 
                             rf'\\begin{{filecontents}}{{references.bib}}\n{reference_content}\n\\end{{filecontents}}', 
                             template_content, 
                             flags=re.DOTALL)

    if output_path is not None:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as file:
            file.write(new_content)
    else:
        return new_content
    print(f"References have been inserted. Output saved to {output_path}")

# test
if __name__ == "__main__":
    template_dir = './'
    template_path = template_dir + 'latex/template.tex'
    reference_path = template_dir + 'sources/source_reference.bib'
    output_path = template_dir + 'temp/template_with_references.tex'

    # 1 restore file with references
    insert_references(template_path, reference_path, output_path)
    # 2 return file content without saving
    insert_references(template_path, reference_path)