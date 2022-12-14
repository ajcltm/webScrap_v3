import unittest
from pathlib import Path
import os
from mock import Mock
from webScrap import work
from typing import List
import pickle
import json

class SimpleScrap(work.Work):

    attr1 : str
    attr2 : int

    def request(self):
        url = f'www.simpleScrap.com/{self.attr1}/{self.attr2}'
        mock_request = Mock()
        mock_request.get.return_value = {'key_1':self.attr1, 'key_2':self.attr2}
        data = mock_request.get()
        return data

class SimpleScraps(work.Works):

    works : List[SimpleScrap]

@unittest.skip("")
class Test_pickle_work(unittest.TestCase):

    def setUp(self) -> None:
        self.folder_path = Path.cwd().joinpath('test', 'test_folder')
        if not os.path.isdir(self.folder_path):
            os.makedirs(self.folder_path)
    
    def tearDown(self) -> None:
        file_list = os.listdir(self.folder_path)
        print(f'saving result : ')
        for file in file_list:
            with open(self.folder_path.joinpath(file), mode='rb') as fr:
                data = pickle.load(fr)
                print(f'data : {data}')

    @unittest.skip('...')
    def test_1_simple_do_work(self):
        scraper = SimpleScrap(attr1='kim', attr2=100)
        scraper.do_work(folder_path=self.folder_path, type='pickle')

    def test_2_simpleWorks_do_work(self):
        lst = [SimpleScrap(attr1='kim', attr2=i) for i in range(0, 139)]
        scrapers = SimpleScraps(works=lst)
        scrapers.do_work(folder_path=self.folder_path, type='pickle')


class Test_json_work(unittest.TestCase):

    def setUp(self) -> None:
        self.folder_path = Path.cwd().joinpath('test', 'test_folder')
        if not os.path.isdir(self.folder_path):
            os.makedirs(self.folder_path)
    
    def tearDown(self) -> None:
        file_list = os.listdir(self.folder_path)
        print(f'saving result : ')
        for file in file_list:
            with open(self.folder_path.joinpath(file)) as fr:
                data = json.load(fr)
                print(f'data : {data}')

    def test_1_simple_do_work(self):
        scraper = SimpleScrap(attr1='kim', attr2=100)
        scraper.do_work(folder_path=self.folder_path, type='json')

    # @unittest.skip('...')
    def test_2_simpleWorks_do_work(self):
        lst = [SimpleScrap(attr1='kim', attr2=i) for i in range(0, 139)]
        scrapers = SimpleScraps(works=lst)
        scrapers.do_work(folder_path=self.folder_path, type='json')

if __name__ == '__main__':
    unittest.main()