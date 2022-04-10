import os
import re
import sys
import textwrap

class ArgumentParser():
    def __init__(self, args=dict) -> None:
        self.args = args

    def validate(self) -> bool:
        # check if regex values are valid
        if self.args.get('r'):
            try:
                re.compile(self.args['q'])
            except re.error as error:
                print('The regex argument is set, therefore all values must be valid regex.\n')
                print('Error message: ' + error.msg)
                print('Pattern: ' + error.pattern)
                print('At position: ' + str(error.pos))
                return False

        return True

class HelpPrinter():
    def __init__(self) -> None:
        # using the whole screen may produce bad formatted output
        # I found this to work for most screen resolutions
        self.max_text_length = int(os.get_terminal_size()[0] * 0.75) - 20

        self.phrases = []
        self.phrases.append('Search for file contents in the osu! wiki.')
        self.phrases.append('\nUsage: [OPTIONS] SEARCH_QUERY [SEARCH_QUERY...]')
        self.phrases.append('\nMaintenance:')
        self.phrases.append('  -h, --help\t\t\tPrint this view.')
        self.phrases.append('  -s, --set [link]\t\tSet the link to the wiki.')
        self.phrases.append('\nSearch options:')
        self.phrases.append('  -d, --dirs\t\t\tSearch only in directory names. Notice: On Windows, you need to use \'\\\' if you want to search via folder paths.')
        self.phrases.append('  -l, --language [language]\tSet specific language. Can be any language the wiki supports (two-letter country code).')
        self.phrases.append('  -r, --regex [regex]\t\tSearch with a regex pattern.')
        self.phrases.append('\nOutput options:')
        self.phrases.append('  -v, --verbose\t\t\tOutput of the entire link to found files.')

    def print(self) -> None:
        for phrase in self.phrases:
            text = textwrap.fill(phrase, subsequent_indent='\t\t\t\t', width=self.max_text_length, replace_whitespace=False)
            print(text)

def print_help():
    h = HelpPrinter()
    h.print()

def try_next_arg(index) -> str:
    try:
        element = sys.argv[index]
    except IndexError:
        element = ''

    return element

def get_args() -> dict:
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

# return path to a file, without the file entry
def get_path(link_to_file) -> str:
    if link_to_file.rfind('\\') == -1:
        path = link_to_file
    else:
        last_occurrence = link_to_file.rfind('\\')
        path = link_to_file[:last_occurrence]
    
    return path

def set_wiki_link(link) -> bool:
    if not os.path.exists(link):
        return False

    path = get_path(sys.executable)
    with open(path + '\\wiki_link.txt', 'w', encoding='utf-8') as w:
        w.write(link)
    
    return True

def get_wiki_link() -> str:
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

def get_root_link(root, verbose_output) -> str:
    if not verbose_output:
        position = root.find('\\wiki\\')

        # remove '\wiki\' from link
        if position != -1:
            return root[position + 6:] + '\\'
        else:
            # there is no subfolder (root ends with '\wiki')
            return ''

    # check if root has subfolder
    if root.endswith('\\wiki'):
        return root

    return root + '\\'

def should_be_excluded(str, exclude_params, use_regex):
    if use_regex:
        for exclude in exclude_params:
            if re.search(exclude, str) is not None:
                return True
    else:
        for exclude in exclude_params:
            if str.find(exclude) != -1:
                return True

    return False

def search_dirs(params) -> list:
    result = []

    for root, dirs, files in os.walk(params['wiki_link']):
        for dir in dirs:
            s = str(get_root_link(root, params['verbose_output']) + dir)

            # don't include image directories
            if s.find(params['query']) != -1 and not s.endswith('img'):
                result.append(s)

    return result

def search_files(params) -> list:
    result = []

    for root, dirs, files in os.walk(params['wiki_link']):
        for file in files:
            with open(root + '/' + file, encoding='utf-8') as f:
                if file.endswith(params['file_type']):
                    data = f.read()

                    if params['use_regex']:
                        if re.search(params['query'], data):
                            s = str(get_root_link(root, params['verbose_output']) + file)
                            result.append(s)
                            continue

                    if data.find(params['query']) != -1:
                        s = str(get_root_link(root, params['verbose_output']) + file)
                        result.append(s)

    return result

def get_result(params) -> list:
    if params['search_dirs']:
        return search_dirs(params)

    return search_files(params)

def main() -> None:
    if len(sys.argv) < 2:
        print('No arguments provided\n')
        print_help()
        return

    parser = ArgumentParser(get_args())
    if not parser.validate():
        return

    if 'h' in parser.args.keys():
        print_help()
        return

    if 's' in parser.args.keys():
        if set_wiki_link(parser.args['s']):
            print('Wiki link has been set to: ' + parser.args['s'])
        else:
            print('This wiki link is not valid.')
        
        return

    # Params for search algorithm
    params = {}

    params['file_type'] = '.md'
    if 'l' in parser.args.keys():
        valid_languages = \
        ['en', 'ar', 'be', 'bg', 'cs', 'da', 'de', 'gr', 'es', 'fi', 'fr',
        'hu', 'id', 'it', 'ja', 'ko', 'nl', 'no', 'pl', 'pt', 'pt-br',
        'ro', 'ru', 'sk', 'sv', 'th', 'tr', 'uk', 'vi', 'zh', 'zh-tw']

        if parser.args['l'] in valid_languages:
            params['file_type'] = parser.args['l'] + '.md'

    params['use_regex'] = False
    if 'r' in parser.args.keys():
        params['use_regex'] = True

    if 'q' not in parser.args.keys():
        print('Query may not be empty!')
        return
    
    params['query'] = parser.args['q']

    params['search_dirs'] = False
    if 'd' in parser.args.keys():
        params['search_dirs'] = True

    params['verbose_output'] = False
    if 'v' in parser.args.keys():
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

if __name__ == '__main__':
    main()
