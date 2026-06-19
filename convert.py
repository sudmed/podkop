import urllib.request
import json

# исходный файл
url = "https://raw.githubusercontent.com/v2rayA/dist-v2ray-rules-dat/refs/heads/master/win-spy.txt"

try:
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
except Exception as e:
    print(f"Ошибка скачивания: {e}")
    exit(1)

domain = []
domain_suffix = []
domain_keyword = []
domain_regex = []

# Парсинг формата v2ray
for line in content.splitlines():
    line = line.strip()
    if not line or line.startswith('#') or line.startswith('include:'):
        continue
    
    if line.startswith('full:'):
        domain.append(line[5:])
    elif line.startswith('domain:'):
        domain_suffix.append(line[7:])
    elif line.startswith('keyword:'):
        domain_keyword.append(line[8:])
    elif line.startswith('regexp:'):
        domain_regex.append(line[7:])
    else:
        # Если префикс не указан, по умолчанию считаем это domain_suffix
        domain_suffix.append(line)

# Формирование правила
rule = {}
if domain: rule["domain"] = domain
if domain_suffix: rule["domain_suffix"] = domain_suffix
if domain_keyword: rule["domain_keyword"] = domain_keyword
if domain_regex: rule["domain_regex"] = domain_regex

# Итоговый JSON-формат для Sing-box / Hiddify
rule_set = {
    "version": 1,
    "rules": [rule] if rule else []
}

with open("win-spy.json", "w", encoding="utf-8") as f:
    json.dump(rule_set, f, indent=2, ensure_ascii=False)

print("Конвертация успешно завершена. Файл win-spy.json создан.")
