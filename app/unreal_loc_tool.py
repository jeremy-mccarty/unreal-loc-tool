import csv, sys, os
from datetime import datetime


SUPPORTED_BATCH_EXTENSIONS = (".csv", ".po")


# ----------------------------
# Utility
# ----------------------------


def detect_language_from_filename(filename):
    name = os.path.basename(filename)
    return os.path.splitext(name)[0]


def escape_po(text):
    return text.replace('"', r"\"")


def build_batch_output_path(input_path, output_dir):
    if not output_dir:
        return None

    os.makedirs(output_dir, exist_ok=True)
    base_name, extension = os.path.splitext(os.path.basename(input_path))

    if extension == ".csv":
        return output_dir
    if extension == ".po":
        return os.path.join(output_dir, f"{base_name}.csv")

    raise ValueError(f"Unsupported file type for batch conversion: {input_path}")


def convert_file(input_path, output_dir=None):
    _, extension = os.path.splitext(input_path)

    if extension == ".csv":
        return csv_to_po(input_path, build_batch_output_path(input_path, output_dir))
    if extension == ".po":
        return po_to_csv(input_path, build_batch_output_path(input_path, output_dir))

    raise ValueError(f"Unsupported file type for conversion: {input_path}")


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


def csv_to_po(
    csv_path: str, output_dir: str | None = None, project_name: str = "Unreal Project"
) -> str:
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

            combined_key = f"{namespace},{key}"

            if combined_key in seen_keys:
                raise ValueError(f"Duplicate key detected: {combined_key}")

            seen_keys.add(combined_key)

            # Write commented out metadata
            pofile.write(f"#. Key: {key}\n")
            if location:
                pofile.write(f"#. SourceLocation: {location}\n")
                pofile.write(f"#: {location}\n")

            pofile.write(f'msgctxt "{combined_key}"\n')
            pofile.write(f'msgid "{escape_po(source)}"\n')
            pofile.write(f'msgstr "{escape_po(translation)}"\n\n')

    result = f"Generated {output_path}"
    print(result)
    return result


# ----------------------------
# PO → CSV
# ----------------------------


def po_to_csv(po_path: str, output_path: str | None = None) -> str:
    if not output_path:
        output_path = os.path.splitext(po_path)[0] + ".csv"

    rows = []

    with open(po_path, encoding="utf-8") as po:
        namespace = key = source = translation = location = ""
        skip_header = True  # flag to ignore the header block

        for line in po:
            line = line.strip()
            if skip_header:
                # Header always starts with msgid "" and ends at the first empty #. Key:
                if line.startswith("#. Key:"):
                    skip_header = False
                continue  # skip everything until header ends

            if line.startswith("#. SourceLocation:"):
                location = line.replace("#. SourceLocation:", "").strip()

            elif line.startswith("msgctxt"):
                combined = line.split('"')[1]
                namespace, key = combined.split(",", 1)

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

    result = f"Generated {output_path}"
    print(result)
    return result


# ----------------------------
# Batch Mode
# ----------------------------


def batch_convert(folder_path, output_dir=None):
    results = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and file.endswith(SUPPORTED_BATCH_EXTENSIONS):
            results.append(convert_file(file_path, output_dir))

    return summarize_batch_results(results)


def batch_convert_recursive(folder_path, targets=None, output_dir=None):
    results = []
    selected_targets = set(targets) if targets is not None else None
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(SUPPORTED_BATCH_EXTENSIONS):
                file_path = os.path.join(root, file)

                if selected_targets is not None and file_path not in selected_targets:
                    continue

                if output_dir:
                    rel_path = os.path.relpath(root, folder_path)
                    file_output_dir = os.path.join(output_dir, rel_path)
                else:
                    file_output_dir = None

                results.append(convert_file(file_path, file_output_dir))

    return summarize_batch_results(results)


def summarize_batch_results(results):
    n = len(results)
    if n == 0:
        result = "Batch convert failed"
    else:
        result = f"Batch convert successful for {n} files:\n"
        result += "\n".join(results) + "\n"

    print(result)
    return result


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
