import os, json, re

d = r'f:\RenPyDevelopment\Projects\DoctorNeonPrototype\game\tl\english_us\game-scripts\chapters\chapter1'
rus_pattern = re.compile(r'^\s*#\s*(?:\"[^\"]+\"|[\w_]+(?:\s+[\w_]+)*)\s+\"([^\"]+)\"')
eng_pattern = re.compile(r'^\s*(?:\"[^\"]+\"|[\w_]+(?:\s+[\w_]+)*)\s+\"\"\s*$')

results = {}

for root, _, files in os.walk(d):
    for f in files:
        if f.endswith('.rpy'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            file_results = []
            for i in range(len(lines) - 1):
                rus_match = rus_pattern.match(lines[i])
                eng_match = eng_pattern.match(lines[i+1])
                
                if rus_match and eng_match:
                    file_results.append(rus_match.group(1))
            
            if file_results:
                results[f] = file_results

with open('untranslated.json', 'w', encoding='utf-8') as out:
    json.dump(results, out, ensure_ascii=False, indent=2)
print("Done")
