# pip install requests pyyaml plyer pyobjus

from plyer import notification
import requests
import re
import time

def getTowerID(towerName):
    towers = requests.post(
        'https://api.cleverschool.cn/washapi4/device/tower', json={}).json()
    for item in towers['data']:
        if item['text'] == towerName:
            return item['value']

def getWashers(towerID, floorNames):
    washersData = requests.post('https://api.cleverschool.cn/washapi4/device/status', json={
        'towerKey': towerID
    }).json()['data']

    washers = []
    for item in washersData:
        if item['floorName'] in floorNames:
            t = item['status'].split()[1]
            if '剩余' in t:
                match = re.search(r'\d+', t)
                timeRemain = int(match.group())
            else:
                timeRemain = 0
            washers.append({
                "floor": item['floorName'],
                "id": item['macUnionCode'],
                "timeRemain": timeRemain})
    return washers

if __name__ == '__main__':
    towerName = '紫荆1号楼'
    floorNames = ['三层']
    towerID = getTowerID(towerName)
    washers = getWashers(towerID, floorNames)
    for index, washer in enumerate(washers):
        print(f'{index}. {washer['floor']} {washer['id']}\t{washer['timeRemain']} 分钟')
    trackWashers = list(map(int, input('Track washers (separated by space): ').split()))
    
    while True:
        print("\033[H\033[J", end="")
        washers = getWashers(towerID, floorNames)
        for index in trackWashers:
            washer = washers[index]
            print(f'{index}. {washer['floor']} {washer['id']}\t{washer['timeRemain']} 分钟')
            if washer['timeRemain'] <= 5:
                notification.notify(
                    title = 'washer-notifier',
                    message = f'{washer['floor']} {washer['id']}\t{washer['timeRemain']} 分钟'
                )
        time.sleep(3)