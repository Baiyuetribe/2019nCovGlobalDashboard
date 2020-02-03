import json
import os
import requests

def get_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r = json.loads(requests.get(url).text)
    with open(os.path.join('data','data.json'),'w',encoding='utf-8') as f:
        f.write(r['data'])

if __name__ == "__main__":
    get_data()