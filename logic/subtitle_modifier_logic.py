import os

def modify_subtitles(input_path, output_path):
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            content = file.read()
        entries = content.split('\n\n')
        common_punctuation = ['.', '?', '!']
        incomplete_indices = []
        for i, entry in enumerate(entries):
            lines = entry.split('\n')
            if len(lines) > 2:
                last_line = lines[-1]
                if not last_line.endswith(tuple(common_punctuation)) or last_line.endswith(','):
                    incomplete_indices.append(i)
        for index in incomplete_indices:
            lines = entries[index].split('\n')
            if lines[-1].endswith((',', ':')):
                lines[-1] = lines[-1]
            else:
                lines[-1] = lines[-1] + "..."
            entries[index] = '\n'.join(lines)
            if index + 1 < len(entries):
                next_lines = entries[index + 1].split('\n')
                if len(next_lines) > 2:
                    next_lines[2] = "..." + next_lines[2]
                    entries[index + 1] = '\n'.join(next_lines)
        modified_content = '\n\n'.join(entries)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(modified_content)
        return f"Subtitles modified successfully! Saved to: {output_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
