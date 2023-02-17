import json
import unittest

from parser_sсript import JSON, clean_record


class Test_parser(unittest.TestCase):
    def setUp(self):
        self.json_item = JSON("./test/test_data.json")
        self.test_data = ['14523      ', '<span>Some phone         </span>',
                '<span>         Some &quot;name&quot; </span>']
    def test_cleaning_data(self):
        self.test_values = clean_record(self.test_data)
        self.assertEqual(self.test_values, {'uid': '14523', 'phone': 'Some phone', 'fio': 'Some "name"'})
    def test_save(self):
        self.json_item.save(clean_record(self.test_data))
        self.json_item.close()

if __name__ == "__main__":
    unittest.main()
