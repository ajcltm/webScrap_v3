from webScrap import saver
from typing import List
from abc import ABC, abstractmethod
import os
from pydantic import BaseModel
from tqdm import tqdm


class Work(ABC):
    
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def get_file_name(self):
        return '_'.join(['_'.join(item) for item in self.dict().items()])
    
    @abstractmethod
    def request(self):
        pass

    def save(self, folder_path, data, type):
        saver_ = saver.Factory_saver().get_saver(type=type)
        saver_(folder_path).save_file(data=data, type=type)

    def do_work(self, folder_path, type):
        data = self.request()        
        self.save(folder_path=folder_path, data=data, type=type)

class Works(BaseModel):
    works : List[Work]

    def filt(self, first_set, other_set):
        return list(set(other_set).difference(set(first_set)))

    def chunk_list(self, lst, num):
        return [lst[i: i+num] for i in range(0, len(lst), num)]
    
    def file_name_to_dict(self, file_name):
        file_name_without_extention = os.path.splitext(file_name)[0]
        element_lst = file_name_without_extention.split('_')
        chunked_lst = self.chunk_list(lst=element_lst, num=2)
        return {i[0] : i[1] for i in chunked_lst}
    
    def get_workedList(self, folder_path):
        file_name_lst = os.listdir(folder_path)
        return [self.works[0].__class__(**self.file_name_to_dict(file_name=file_name)) for file_name in tqdm(file_name_lst, desc='now getting the worked list : ')]
    
    def do_work(self, folder_path, type):
        workedList = self.get_workedList(folder_path) 
        toWorkList = self.filt(first_set=workedList, other_set=self.works)
        for work in tqdm(toWorkList, desc='now working on process'):
            work.do_work(folder_path=folder_path, type=type)
