import json
from difflib import unified_diff

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_diff(diff_lines):
    changes = []
    removed = []
    added = []

    for line in diff_lines:
        if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
            continue  # Skip diff metadata lines
        elif line.startswith('-'):
            removed.append(line[1:].strip())
        elif line.startswith('+'):
            added.append(line[1:].strip())
        else:
            # Commit any pending added/removed as a "modified" block
            if removed or added:
                change_type = "modified"
                if removed and not added:
                    change_type = "removed"
                elif added and not removed:
                    change_type = "added"

                changes.append({
                    "type": change_type,
                    "original_text": "\n".join(removed) if removed else None,
                    "updated_text": "\n".join(added) if added else None
                })
                removed = []
                added = []

    # Handle any remaining
    if removed or added:
        change_type = "modified"
        if removed and not added:
            change_type = "removed"
        elif added and not removed:
            change_type = "added"

        changes.append({
            "type": change_type,
            "original_text": "\n".join(removed) if removed else None,
            "updated_text": "\n".join(added) if added else None
        })

    return changes

def compare_documents(file1, file2, output_file):
    doc1 = load_json(file1)
    doc2 = load_json(file2)

    max_pages = max(len(doc1), len(doc2))
    comparison_result = []

    for i in range(max_pages):
        page1_text = doc1[i]["text"] if i < len(doc1) else ""
        page2_text = doc2[i]["text"] if i < len(doc2) else ""

        is_identical = page1_text == page2_text
        diff = list(unified_diff(
            page1_text.splitlines(),
            page2_text.splitlines(),
            fromfile=f'File1_Page{i+1}',
            tofile=f'File2_Page{i+1}',
            lineterm=''
        ))

        parsed_changes = parse_diff(diff) if not is_identical else []

        comparison_result.append({
            "page_number": i + 1,
            "is_identical": is_identical,
            "changes": parsed_changes
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(comparison_result, f, indent=2, ensure_ascii=False)

    print(f"✅ Comparison saved to {output_file}")

# Example usage
compare_documents('Elite_text.json', 'Infinite_text.json', 'comparison_output.json')

