def read_country_file(file: str) -> list:
    lines = []
    with open(file, mode='r', encoding='utf-8', newline='\n') as r:
        lines = r.readlines()

    # remove newline character
    for index, line in enumerate(lines):
        lines[index] = line[:-1]

    return lines

def replace_country_in_line(line: str, target: dict) -> str:
    for key, value in target.items():
        line = line.replace(key, value)

    return line

def translate_countries(file: str, target: dict) -> None:
    lines = []
    with open(file, mode='r', encoding='utf-8', newline='\n') as r:
        lines = r.readlines()

        for line_index, line in enumerate(lines):
            new_line = replace_country_in_line(line, target)
            lines[line_index] = new_line

    with open(file, mode='w', encoding='utf-8', newline='\n') as w:
        w.writelines(lines)

def main() -> None:
    origin = read_country_file('en.txt')
    target = read_country_file('de.txt')

    countries = {}
    for index, country in enumerate(origin):
        countries[country] = target[index]

    translate_countries('de.md', countries)

if __name__ == '__main__':
    main()
