import os
import re
import sys

def print_help():
    print('Usage:')
    print('  -d, --dirs\t\t\tSearch only in directory names. Notice: On Windows, you need to use \'\\\' if you want to search via folder paths.')
    print('  -h, --help\t\t\tPrint this view.')
    print('  -l, --language [language]\tSet specific language. Can be any language the wiki supports.')
    print('  -r, --regex\t\t\tSearch with a regex pattern.')
    print('  -s, --set\t\t\tSet the link to the wiki.')
    print('  -v, --verbose\t\t\tOutput of the entire link to found files.')

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

        if sys.argv[i] == '-d' or sys.argv[i] == '--dirs':
            args.update({'d': ''})
            i = i + 1
            continue

        if sys.argv[i] == '-v' or sys.argv[i] == '--verbose':
            args.update({'v': ''})
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

    try:
        f = open(path + '\\wiki_link.txt', 'r', encoding='utf-8')
        link_data = f.read()
        f.close()

        if link_data:
            return link_data

        return ''
    except FileNotFoundError:
        return ''

def get_root_link(root, verbose_output):
    if not verbose_output:
        position = root.find('\\wiki\\')
        if position != -1:
            # remove '\wiki\' from link
            return root[position + 6:]
    
    return root

def get_result(params):
    result = []

    for root, dirs, files in os.walk(params['wiki_link']):
        if params['search_dirs']:
            for dir in dirs:
                s = str(get_root_link(root, params['verbose_output']) + '\\' + dir)

                # don't include image directories
                if s.find(params['query']) != -1 and not s.endswith('img'):
                    result.append(s)
            continue

        for file in files:
            with open(root + '/' + file, encoding='utf-8') as f:
                if file.endswith(params['file_type']):
                    data = f.read()

                    if params['use_regex']:
                        if re.search(params['query'], data):
                            s = str(get_root_link(root, params['verbose_output']) + '\\' + file)
                            result.append(s)
                            continue

                    if data.find(params['query']) != -1:
                        s = str(get_root_link(root, params['verbose_output']) + '\\' + file)
                        result.append(s)
            f.close()

    return result

def main():
    if len(sys.argv) < 2:
        print('No arguments provided\n')
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

    # Params for search algorithm
    params = {}

    params['file_type'] = '.md'
    if 'l' in args.keys():
        valid_languages = \
        ['en', 'ar', 'be', 'bg', 'cs', 'da', 'de', 'gr', 'es', 'fi', 'fr',
        'hu', 'id', 'it', 'ja', 'ko', 'nl', 'no', 'pl', 'pt', 'pt-br',
        'ro', 'ru', 'sk', 'sv', 'th', 'tr', 'uk', 'vi', 'zh', 'zh-tw']

        if args['l'] in valid_languages:
            params['file_type'] = args['l'] + '.md'

    params['use_regex'] = False
    if 'r' in args.keys():
        params['use_regex'] = True

    if 'q' not in args.keys():
        print('Query may not be empty!')
        return
    
    params['query'] = args['q']

    params['search_dirs'] = False
    if 'd' in args.keys():
        params['search_dirs'] = True

    params['verbose_output'] = False
    if 'v' in args.keys():
        params['verbose_output'] = True
    
    wiki_link = get_wiki_link()
    if not wiki_link:
        print('Not a valid wiki link. Try setting the link via -s or --set.')
        return

    params['wiki_link'] = wiki_link
    
    result = get_result(params)

    # Print result
    for s in result:
        print(s)

    if len(result) == 1:
        result_text = str(len(result)) + ' occurrence was found.'
    else:
        result_text = str(len(result)) + ' occurrences were found.'
    print(result_text)

main()
