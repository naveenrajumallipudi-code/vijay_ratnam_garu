import fitz  # PyMuPDF
import re
import json

PDF_FILE = "question bank CLI 2023 (1)(4).pdf"
OUTPUT_FILE = "questions.json"


# -----------------------------
# Read PDF
# -----------------------------
def read_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        try:
            text += page.get_text("text")
            text += "\n"
        except:
            pass

    doc.close()
    return text


# -----------------------------
# Clean text
# -----------------------------
def clean_text(text):

    text = text.replace("\r", "\n")
    text = text.replace("\t", " ")

    while "  " in text:
        text = text.replace("  ", " ")

    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    return text


# -----------------------------
# Regular Expressions
# -----------------------------

QUESTION_PATTERN = re.compile(
    r'^\s*(\d+)\.\s*(.+)',
    re.MULTILINE
)

OPTION_PATTERN = re.compile(
    r'^\s*\(([ABCD])\)\s*(.+)',
    re.MULTILINE
)

ANSWER_PATTERN = re.compile(
    r'\(([ABCD])\)\s*$'
)


# -----------------------------
# Read File
# -----------------------------

raw_text = read_pdf(PDF_FILE)
raw_text = clean_text(raw_text)

lines = raw_text.split("\n")

questions = []

current_question = None
current_options = []

for line in lines:

    line = line.strip()

    if line == "":
        continue

    q = QUESTION_PATTERN.match(line)

    if q:

        if current_question is not None:

            while len(current_options) < 4:
                current_options.append("")

            questions.append({
                "question": current_question,
                "options": current_options[:4],
                "answer": -1
            })

        current_question = q.group(2)

        current_options = []

        continue

    op = OPTION_PATTERN.match(line)

    if op:

        current_options.append(op.group(2))

        continue

    if current_question is not None:

        if len(current_options) == 0:
            current_question += " " + line
        else:
            current_options[-1] += " " + line


if current_question:

    while len(current_options) < 4:
        current_options.append("")

    questions.append({
        "question": current_question,
        "options": current_options[:4],
        "answer": -1
    })


print("Questions Found :", len(questions))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=4, ensure_ascii=False)

print("Saved to", OUTPUT_FILE)