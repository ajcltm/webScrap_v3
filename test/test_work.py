import unittest
from pathlib import Path
import os
from mock import Mock
from webScrap import work
import pickle

class SimpleScrap(work.Work):

    attr1 : str
    attr2 : int

    def request(self):
        url = f'www.simpleScrap.com/{self.attr1}/{self.attr2}'
        mock_request = Mock()
        mock_request.get.return_value = {'key_1':self.attr1, 'key_2':self.attr2}
        data = mock_request.get()
        return data


class Test_work(unittest.TestCase):

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
        lst = [SimpleScrap(attr1='kim', attr2=i) for i in range(0, 129)]
        scrapers = work.Works(works=lst)
        scrapers.do_work(folder_path=self.folder_path, type='pickle')


if __name__ == '__main__':
    unittest.main()