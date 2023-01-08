from webScrap import saver
from abc import ABC, abstractmethod
import os
from pydantic import BaseModel 
from tqdm import tqdm
import random
import time


class Work(ABC, BaseModel):
    
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def get_file_name(self):
        return '_'.join([f'{key}_{value}' for key, value in self.dict().items()])
    
    @abstractmethod
    def request(self):
        pass

    def save(self, folder_path, data, type):
        saver_ = saver.Factory_saver().get_saver(type=type)
        saver_(folder_path).save_file(data=data, file_name=self.get_file_name(), type=type)

    def do_work(self, folder_path, type='json'):
        data = self.request()        
        self.save(folder_path=folder_path, data=data, type=type)

class Works(BaseModel):

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
        if file_name_lst:
            return [list(self.__dict__.values())[0][0].__class__(**self.file_name_to_dict(file_name=file_name)) for file_name in tqdm(file_name_lst, desc='now getting the worked list : ')]
        return None
    
    def random_sleep(self, intv_mtple):
        range_option = {'quicker': [0, .5], 'slower': [.5, 2], 'stop': [10, 15]}
        sleepLevel = random.choices(['quicker', 'slower', 'stop'], weights=[.6, .39, .01])
        range = range_option.get(sleepLevel[0])
        time.sleep(random.uniform(range[0]*intv_mtple, range[1]*intv_mtple))
    
    def do_work(self, folder_path, type, intv_mtple=1):
        workedList = self.get_workedList(folder_path) 
        if workedList:
            toWorkList = self.filt(first_set=workedList, other_set=list(self.__dict__.values())[0])
        else:
            toWorkList = list(self.__dict__.values())[0]
        for work in tqdm(toWorkList, desc='now working on process'):
           work.do_work(folder_path=folder_path, type=type)
           self.random_sleep(intv_mtple=intv_mtple)
