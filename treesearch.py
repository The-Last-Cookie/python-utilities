import os
import re
import sys

def print_help():
    print('No arguments provided\n')
    print('Usage:')
    print('\t-h, --help\tPrint this view.')
    print('\t-l, --language\tSet specific language. Can be any language the wiki supports.')
    print('\t-r, --regex\tSearch with a regex pattern.')
    print('\t-s, --set\tSet the link to the wiki.')

def try_next_arg(index):
    try:
        element = sys.argv[index]
    except IndexError:
        element = ''

    return element

def get_args():
    args = {}
    # Skip file name argument
    i = 1

    while(i < len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            args.update({'h': ''})
            i = i + 1
            continue

        if sys.argv[i] == '-s' or sys.argv[i] == '--set':
            next_arg = try_next_arg(i + 1)
            args.update({'s': next_arg})
            i = i + 2
            continue

        if sys.argv[i] == '-l' or sys.argv[i] == '--language':
            next_arg = try_next_arg(i + 1)
            args.update({'l': next_arg})
            i = i + 2
            continue

        if sys.argv[i] == '-r' or sys.argv[i] == '--regex':
            args.update({'r': ''})
            i = i + 1
            continue

        if 'q' not in args.keys():
            args.update({'q': sys.argv[i]})
        else:
            new_query = args['q'] + ' ' + sys.argv[i]
            args.update({'q': new_query})

        i = i + 1

    return args

def get_path(link_to_file):
    if link_to_file.rfind('\\') == -1:
        path = link_to_file
    else:
        last_occurrence = link_to_file.rfind('\\')
        path = link_to_file[:last_occurrence]
    
    return path

def set_wiki_link(link):
    if not os.path.exists(link):
        return False

    path = get_path(sys.executable)
    with open(path + '\\wiki_link.txt', 'w', encoding='utf-8') as w:
        w.write(link)
    
    return True

def get_wiki_link():
    path = get_path(sys.executable)
    f = open(path + '\\wiki_link.txt', 'r', encoding='utf-8')
    link_data = f.read()
    f.close()

    if link_data:
        return link_data

    return ''

def get_result(wiki_link, file_type, query, use_regex):
    result = []

    if not query:
        print('Query may not be empty!')
        return

    for root, dirs, files in os.walk(wiki_link):
        if root.find(query) != -1:
            s = str(root)
            result.append(s)

        for file in files:
            with open(root + '/' + file, encoding='utf-8') as f:
                if file.endswith(file_type):
                    data = f.read()

                    if use_regex:
                        if re.search(query, data):
                            s = str(root + '/' + file)
                            result.append(s)
                            continue
                        
                    if data.find(query) != -1:
                        s = str(root + '/' + file)
                        result.append(s)
            f.close()

    return result

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    args = get_args()

    if 'h' in args.keys():
        print_help()
        return

    if 's' in args.keys():
        if set_wiki_link(args['s']):
            print('Wiki link has been set to: ' + args['s'])
        else:
            print('This wiki link is not valid.')
        
        return

    file_type = '.md'
    if 'l' in args.keys():
        valid_languages = \
        ['en', 'ar', 'be', 'bg', 'cs', 'da', 'de', 'gr', 'es', 'fi', 'fr',
        'hu', 'id', 'it', 'ja', 'ko', 'nl', 'no', 'pl', 'pt', 'pt-br',
        'ro', 'ru', 'sk', 'sv', 'th', 'tr', 'uk', 'vi', 'zh', 'zh-tw']

        if args['l'] in valid_languages:
            file_type = args['l'] + '.md'

    use_regex = False
    if 'r' in args.keys():
        use_regex = True

    query = ''
    if 'q' in args.keys():
        query = args['q']

    wiki_link = get_wiki_link()
    if not wiki_link:
        print('Not a valid wiki link. Try setting the link via -s or --set.')
        return
    
    result = get_result(wiki_link, file_type, query, use_regex)

    result_text = 'These occurrences were found (' + str(len(result)) + '):'
    print(result_text)
    for s in result:
        print(s)

main()
