from unittest import TestCase
from unittest import main as testing

import search

class TestGetRootLink(TestCase):
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

class TestShouldBeExcluded(TestCase):
    def test_should_not_exclude_on_empty_params(self):
        b = search.should_be_excluded('', [], True)
        self.assertFalse(b)
        b = search.should_be_excluded('', [], False)
        self.assertFalse(b)

class TestFileTypeInFiles(TestCase):
    def test_return_true_for_default_file_type(self):
        b = search.file_type_in_files('.md', [])
        self.assertTrue(b)
        b = search.file_type_in_files('.md', ['en.md'])
        self.assertTrue(b)
        b = search.file_type_in_files('.md', ['en.md', 'de.md'])
        self.assertTrue(b)

    def test_return_true_if_file_type_in_files(self):
        b = search.file_type_in_files('en.md', ['en.md'])
        self.assertTrue(b)
        b = search.file_type_in_files('en.md', ['en.md', 'de.md'])
        self.assertTrue(b)
        b = search.file_type_in_files('en.md', ['de.md', 'en.md'])
        self.assertTrue(b)

    def test_return_false_if_file_type_not_in_files(self):
        b = search.file_type_in_files('en.md', [])
        self.assertFalse(b)
        b = search.file_type_in_files('en.md', ['de.md'])
        self.assertFalse(b)

if __name__ == '__main__':
    testing()
