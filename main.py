import os
from datetime import datetime
import requests
import json
import random
import logging
import line_bot

from dotenv import load_dotenv
load_dotenv()

os_path = os.getenv('os_path')
my_number = list(map(int, os.getenv('my_number').split(',')))

os.chdir(os_path)
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

eggs_list = ["雞蛋", "鴨蛋", "鵝蛋", "鵪鶉蛋", "鸚鵡蛋", "鴕鳥蛋", "鴿子蛋", "鷹蛋", "鵰蛋", "天鵝蛋", "火雞蛋", "孔雀蛋", "龍蛋"]

today_month = datetime.today().strftime('%Y-%m')
today = datetime.today().strftime('%Y-%m-%d')

def dumpJson(data):
    with open(file_path, 'w') as file:
        json.dump(data, file)

def main():
    url = f"https://api.taiwanlottery.com/TLCAPIWeB/Lottery/Lotto649Result?period&month={today_month}&pageNum=1&pageSize=50"
    result = requests.get(url, timeout=30000)
    req = result.json()

    lotto649Res = {}
    for data in req["content"]["lotto649Res"]:
        lotteryDate = str(data['lotteryDate']).split("T")[0]
        lottery = {}
        lottery['period'] = data['period']
        lottery['drawNumberSize'] = data['drawNumberSize'][:-1]
        lottery['special-number'] = data['drawNumberSize'][-1]
        lottery['jackpotAssign'] = data['jackpotAssign']['perPrize']
        lottery['secondAssign'] = data['secondAssign']['perPrize']
        lottery['thirdAssign'] = data['thirdAssign']['perPrize']
        lottery['fourthAssign'] = data['fourthAssign']['perPrize']
        lottery['fifthAssign'] = data['fifthAssign']['perPrize']
        lottery['sixthAssign'] = data['sixthAssign']['perPrize']
        lottery['seventhAssign'] = data['seventhAssign']['perPrize']
        lottery['normalAssign'] = data['normalAssign']['perPrize']
        lotto649Res[lotteryDate] = lottery


    lottoAssign = {
        '6_0': 'jackpotAssign',
        '5_1': 'secondAssign',
        '5_0': 'thirdAssign',
        '4_1': 'fourthAssign',
        '4_0': 'fifthAssign',
        '3_1': 'sixthAssign',
        '2_1': 'seventhAssign',
        '3_0': 'normalAssign',
    }

    special_number = 0
    try:
        today_nub_info = lotto649Res[today]
    except:
        raise ValueError('尚未取得開獎')
    if today_nub_info['special-number'] in my_number:
        special_number = 1
        my_number.remove(today_nub_info['special-number'])
    numbers = [num for num in my_number if num in today_nub_info['drawNumberSize']]
    RedeemPrize = f"{len(numbers)}_{special_number}"
    Prize = lottoAssign.get(RedeemPrize, 'notPrize')
    prizeAssign = lotto649Res[today].get(Prize, 0)

    text = f"今日 {today} 第{today_nub_info['period']}期\n開獎號碼: \n\t{today_nub_info['drawNumberSize']} \n特別號: \n\t{[today_nub_info['special-number']]}\n\
    我們中獎的號碼: {numbers if numbers else random.choice(eggs_list)}\n\
    我們中獎的金額: {prizeAssign if prizeAssign != 0 else random.choice(eggs_list)}"
    
    line_bot.bot(text)

if __name__ == "__main__":
    file_path = 'status.json'
    if not os.path.exists(file_path):
        dumpJson({})

    status = True
    try:
        status_load = json.load(open(file_path,'r'))
        status = False if status_load[today] == 'done' else True
        logging.info(f'{today} Today has Successfully fetched lottery numbers')
    except:
        pass
    
    if status:
        try:
            main()
            dumpJson({today:'done'})
            logging.info('Successfully fetched lottery numbers')
        except Exception as error:
            dumpJson({today:'error'})
            logging.error(f'Error fetching lottery numbers: {error}')
