import re

# Ruta base
file_path = "input_lista_genus.txt"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

clean_text = re.sub(r"{\\.*?}|\\[a-z]+\d* ?|[{}\\]", "", content)

lines = clean_text.splitlines()
lines_clean = [line.strip() for line in lines if line.strip()]

print(lines_clean)
