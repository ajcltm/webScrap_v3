from typing_extensions import Protocol
from pathlib import Path
import pickle

class IFileSaver(Protocol):

    def save_file(self, data:any, file_name:str, save_extention=str):
        ...

class Factory_saver:

    def get_saver(self, type):
        option = {'pickle':PickleSaver, 'general':GeneralSaver}
        return option.get(type)


class PickleSaver:

    def __init__(self, filePath:Path):
        self.filePath = filePath

    def save_file(self, data:any, file_name, type='pickle') -> None:
        save_path = self.filePath.joinpath(f'{file_name}.{type}')
        with open(save_path, 'wb') as fw:
            pickle.dump(data, fw, protocol=pickle.HIGHEST_PROTOCOL)

class GeneralSaver:

    def __init__(self, filePath:Path):
        self.filePath = filePath

    def save_file(self, data:any, file_name, type) -> None:
        save_path = self.filePath.joinpath(f'{file_name}.{type}')
        with open(save_path, 'wb') as fw:
            fw.write(data)



if __name__ == '__main__':
    import requests
    import json
    from pathlib import Path

    # url = 'https://www.alio.go.kr/download/rulefiledown.json?fileNo=94205'

    # data = requests.get(url).content

    # file_path = Path().home().joinpath('Desktop', 'alio')
    # file_name = '요령 2-4(보수규정시행요령)_191212'
    # FSaver().get_saver(file_extention='hwp')(file_path).save_file(data=data, file_name=file_name, file_extention='hwp')

    url = 'https://www.alio.go.kr/item/itemOrganListSusi.json'
    params = {
        'apbaType': [], 
        'jidtDptm': ["A1020"], 
        'area': [], 
        'apbaId': "", 
        'reportFormRootNo': "21110"
    }
    print(json.dumps(params))

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '85',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'elevisor_for_j2ee_uid=0w1tq30fn33t8; JSESSIONID=surscV2zo66qI7ae3XH97OIGpMMG3QKWVVcKXR7K.portal10',
        'Host': 'www.alio.go.kr',
        'Origin': 'https://www.alio.go.kr',
        'Pragma': 'no-cache',
        'Referer': 'https://www.alio.go.kr/item/itemOrganList.do?reportFormRootNo=21110',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

    data = requests.post(url, data=json.dumps(params), headers=headers).json()
    file_path = Path().home().joinpath('Desktop', 'alio')
    file_name = '중기부 산하기관'
    FSaver().get_saver(save_extention='pickle')(file_path).save_file(data=data, file_name=file_name, save_extention='pickle')

    file = file_path.joinpath(file_name+'.pickle')
    with open(file, 'rb') as fr:
        data = pickle.load(fr)
    print(data)