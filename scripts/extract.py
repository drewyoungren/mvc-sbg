from bs4 import BeautifulSoup
from pathlib import Path
import json

INPUT_DIR = Path("slides")
OUTPUT_JSON = Path("learning_objectives.json")

results = []

file_paths = list(INPUT_DIR.glob("*.html"))
file_paths.sort()

for file_path in file_paths:
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    title = soup.title.string.split('-')[1].strip() if soup.title else file_path.stem
    print(title)
    outcomes_section = soup.select_one("section#learning-outcomes")

    if outcomes_section:
        items = [li.get_text(strip=True) for li in outcomes_section.find_all("li")]
    else:
        items = []

    results.append({
        "file": file_path.name,
        "title": title,
        "objectives": items
    })

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
