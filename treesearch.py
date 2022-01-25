import os
import re

PATH = r''
FILE_TYPE = '.md'
QUERY = ''
REGEX = 0

result = []

if not FILE_TYPE:
    print('File type may not be empty!')
    exit(-1)

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

                if REGEX:
                    if re.match(QUERY, data):
                        s = str(root + '/' + file)
                        result.append(s)
                        continue
                
                if data.find(QUERY) != -1:
                    s = str(root + '/' + file)
                    result.append(s)
        f.close()

result_text = 'These occurrences were found (' + str(len(result)) + '):'
print(result_text)
for s in result:
    print(s)
