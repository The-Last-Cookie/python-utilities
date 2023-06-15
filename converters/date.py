# TODO: use regex group capture
# \((\d{4})-(\d{2})-(\d{2})\)
# ($3.$2.$1)

from datetime import datetime
import re

MONTHS = [
    'Januar',
    'Februar',
    'März',
    'April',
    'Mai',
    'Juni',
    'Juli',
    'August',
    'September',
    'Oktober',
    'November',
    'Dezember'
]

def change_date_in_line(line: str, o_format: str, t_format: str) -> str:
    """
    o_format: Original format that should be replaced
    t_format: Format to convert to
    """
    iter = re.finditer(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', line)
    matches = []

    for m in iter:
        match = line[m.start(0):m.end(0)]
        matches.append(match)

    for match in matches:
        o_date = datetime.strptime(match, o_format)
        t_date = o_date.strftime(t_format)
        line = line.replace(match, t_date)

    iter = re.finditer(r'[0-9]{4}-[0-1][0-9]', line)
    matches = []

    for m in iter:
        string = line[m.start(0):m.end(0)]
        match = {
            'string': string,
            'year': string[0:4],
            'month': string[5:]
        }
        matches.append(match)

    for match in matches:
        month_name = MONTHS[int(match['month']) - 1]
        new_date = month_name + ' ' + match['year']
        line = line.replace(match['string'], new_date)

    return line

def change_date(file: str) -> None:
    lines = []
    with open(file, mode='r', encoding='utf-8', newline='\n') as r:
        lines = r.readlines()

        for line_index, line in enumerate(lines):
            new_line = change_date_in_line(line, '%Y-%m-%d', '%d.%m.%Y')
            lines[line_index] = new_line

    with open(file, mode='w', encoding='utf-8', newline='\n') as w:
        w.writelines(lines)

def main() -> None:
    change_date('de.md')

if __name__ == '__main__':
    main()
