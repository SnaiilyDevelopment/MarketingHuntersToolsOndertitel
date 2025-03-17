from docx import Document
import re

def srt_to_cleaned_word(srt_file_paths, output_file_path):
    try:
        doc = Document()

        for srt_file_path in srt_file_paths:
            with open(srt_file_path, 'r', encoding='utf-8') as file:
                srt_content = file.readlines()

            full_text = ""

            for line in srt_content:
                if '-->' in line or line.strip().isdigit():
                    continue
                full_text += line.strip() + " "

            full_text = re.sub(r'\s+', ' ', full_text).strip()

            paragraphs = re.split(r'(?<=\.)\s+(?=[A-Z])', full_text)

            for para in paragraphs:
                if para.strip().isdigit():
                    continue
                p = doc.add_paragraph(para.strip())
                for run in p.runs:
                    run.font.name = 'Arial' ### Font Change

        doc.save(output_file_path)
        return f"Document saved successfully to {output_file_path}"

    except Exception as e:
        return f"An error occurred: {e}"
