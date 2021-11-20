import os

PATH = r''
FILE_TYPE = '.md'
QUERY = ''

result = []

if not QUERY:
    print('Query may not be empty!')
    exit(-1)

for root, dirs, files in os.walk(PATH):
    if root.find(QUERY) != -1:
        s = str(root)
        result.append(s)

    for file in files:
        with open(root + '/' + file, encoding='utf-8') as f:
            if file.endswith(FILE_TYPE):
                data = f.read()

                if data.find(QUERY) != -1:
                    s = str(root + '/' + file)
                    result.append(s)
        f.close()

print('These occurences were found: ')
for s in result:
    print(s)
