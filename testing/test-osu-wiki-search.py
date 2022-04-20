import unittest

import search

class TestGetRootLink(unittest.TestCase):
    def test_return_whole_link(self):
        s = search.get_root_link('osu-wiki\\wiki', True)
        self.assertEqual(s, 'osu-wiki\\wiki\\')

    def test_return_whole_link_main_folder(self):
        s = search.get_root_link('osu-wiki\\wiki\\S', True)
        self.assertEqual(s, 'osu-wiki\\wiki\\S\\')

    def test_return_whole_link_one_subfolder(self):
        s = search.get_root_link('osu-wiki\\wiki\\S\\T', True)
        self.assertEqual(s, 'osu-wiki\\wiki\\S\\T\\')

    def test_return_whole_link_two_subfolder(self):
        s = search.get_root_link('osu-wiki\\wiki\\S\\T\\Z', True)
        self.assertEqual(s, 'osu-wiki\\wiki\\S\\T\\Z\\')

    def test_return_partial_link(self):
        s = search.get_root_link('osu-wiki\\wiki', False)
        self.assertEqual(s, '')

    def test_return_partial_link_main_folder(self):
        s = search.get_root_link('osu-wiki\\wiki\\S', False)
        self.assertEqual(s, 'S\\')

    def test_return_partial_link_one_subfolder(self):
        s = search.get_root_link('osu-wiki\\wiki\\S\\T', False)
        self.assertEqual(s, 'S\\T\\')

    def test_return_partial_link_two_subfolder(self):
        s = search.get_root_link('osu-wiki\\wiki\\S\\T\\Z', False)
        self.assertEqual(s, 'S\\T\\Z\\')

if __name__ == '__main__':
    unittest.main()
