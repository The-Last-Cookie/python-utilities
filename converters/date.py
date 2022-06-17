from datetime import datetime
import re

def change_date_in_line(line: str, o_format: str, t_format: str) -> str:
    iter = re.finditer(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', line)
    matches = []

    for m in iter:
        match = line[m.start(0):m.end(0)]
        matches.append(match)

    for match in matches:
        o_date = datetime.strptime(match, o_format)
        t_date = o_date.strftime(t_format)
        line = line.replace(match, t_date)

    return line

def change_date(file: str, o_format: str, t_format: str) -> None:
    """
    o_format: Original format that should be replaced
    t_format: Format to convert to
    """
    lines = []
    with open(file, mode='r', encoding='utf-8', newline='\n') as r:
        lines = r.readlines()

        for line_index, line in enumerate(lines):
            new_line = change_date_in_line(line, o_format, t_format)
            lines[line_index] = new_line

    with open(file, mode='w', encoding='utf-8', newline='\n') as w:
        w.writelines(lines)

def main() -> None:
    change_date('de.md', '%Y-%m-%d', '%d.%m.%Y')

if __name__ == '__main__':
    main()
