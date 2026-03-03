import csv
import sys
import os
from datetime import datetime


# ----------------------------
# Utility
# ----------------------------


def detect_language_from_filename(filename):
    name = os.path.basename(filename)
    return os.path.splitext(name)[0]


def escape_po(text):
    return text.replace('"', r"\"")


# ----------------------------
# CSV → PO
# ----------------------------


def write_po_header(outfile, project_name, language):
    outfile.write('msgid ""\n')
    outfile.write('msgstr ""\n')
    outfile.write(f'"Project-Id-Version: {project_name}\\n"\n')
    outfile.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
    outfile.write('"Content-Transfer-Encoding: 8bit\\n"\n')
    outfile.write(f'"Language: {language}\\n"\n')
    outfile.write(
        f'"POT-Creation-Date: {datetime.utcnow().strftime("%Y-%m-%d %H:%M+0000")}\\n"\n\n'
    )


def csv_to_po(csv_path, output_dir=None, project_name="Unreal Project"):
    language = detect_language_from_filename(csv_path)
    po_filename = f"{language}.po"

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, po_filename)
    else:
        output_path = po_filename

    seen_keys = set()

    with open(csv_path, newline="", encoding="utf-8") as csvfile, open(
        output_path, "w", encoding="utf-8"
    ) as pofile:

        reader = csv.DictReader(csvfile)
        write_po_header(pofile, project_name, language)

        for row in reader:
            namespace = row["Namespace"]
            key = row["Key"]
            source = row["Source"]
            translation = row["Translation"]
            location = row.get("SourceLocation", "")

            combined_key = f"{namespace}.{key}"

            if combined_key in seen_keys:
                raise ValueError(f"Duplicate key detected: {combined_key}")

            seen_keys.add(combined_key)

            if location:
                pofile.write(f"#. SourceLocation: {location}\n")

            pofile.write(f'msgctxt "{combined_key}"\n')
            pofile.write(f'msgid "{escape_po(source)}"\n')
            pofile.write(f'msgstr "{escape_po(translation)}"\n\n')
            
    result =f"Generated {output_path}"
    print(result)
    return result


# ----------------------------
# PO → CSV
# ----------------------------


def po_to_csv(po_path, output_path=None):
    if not output_path:
        output_path = os.path.splitext(po_path)[0] + ".csv"

    rows = []

    with open(po_path, encoding="utf-8") as pofile:
        namespace = key = source = translation = location = ""

        for line in pofile:
            line = line.strip()

            if line.startswith("#. SourceLocation:"):
                location = line.replace("#. SourceLocation:", "").strip()

            elif line.startswith("msgctxt"):
                combined = line.split('"')[1]
                namespace, key = combined.split(".", 1)

            elif line.startswith("msgid"):
                source = line.split('"')[1]

            elif line.startswith("msgstr"):
                translation = line.split('"')[1]
                rows.append(
                    {
                        "Namespace": namespace,
                        "Key": key,
                        "Source": source,
                        "Translation": translation,
                        "SourceLocation": location,
                    }
                )
                location = ""

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Namespace", "Key", "Source", "Translation", "SourceLocation"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    result =f"Generated {output_path}"
    print(result)
    return result


# ----------------------------
# Batch Mode
# ----------------------------


def batch_convert(folder_path, output_dir=None):
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            csv_to_po(os.path.join(folder_path, file), output_dir)


# ----------------------------
# CLI
# ----------------------------


def print_usage():
    print(
        """
Usage:

Single file:
  python unreal_loc_tool.py csv2po input.csv [output_dir]
  python unreal_loc_tool.py po2csv input.po [output.csv]

Batch folder:
  python unreal_loc_tool.py batch folder_path [output_dir]
"""
    )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "csv2po":
        csv_to_po(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)

    elif mode == "po2csv":
        po_to_csv(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)

    elif mode == "batch":
        batch_convert(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)

    else:
        print_usage()
