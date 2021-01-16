import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
ans = []
for i in range(1, 11300):  # 取得したいゾーン。1000ごとに40分くらいかかる
    if i % 20 == 0:
        print(i)
    time.sleep(1)
    res = requests.get(
        f'http://play-agricola.com/Agricola/Cards/index.php?id={i}')
    soup = BeautifulSoup(res.text, 'html.parser')
    # [playagricolaid,cardname,cardtext,cost,vp,Prereq,occtype,bonus.passing]
    result = [i, None, None, None, None, None, None, None, None]
    soup2 = soup.find('span')
    check = re.search(
        r'span style=\'display:none\'[\s\S]*?.javascript:quote', str(soup2))
    if not check:
        continue
    result[7] = re.search(
        r'id\=\'bonus[0-9]+\' value=\'[0-9]\'', str(soup2)).group()[-2]
    result[8] = re.search(
        r'id\=\'pass[0-9]+\' value=\'[0-9]\'', str(soup2)).group()[-2]
    tmp = check.group()
    minor = re.search(r'&gt;.*\(minor', tmp)
    occ = re.search(r'&gt;.*\(occ', tmp)
    if minor:
        result[1] = minor.group()[4:-7]
        text = re.search(r'minor[\s\S]*forum', tmp).group()
        text2 = text[re.search(r'br&gt', text).end():]
        text3 = text2[re.search(r'br&gt', text2).end():]
        result[2] = text3[:re.search(r'br&gt', text3).start(
        )-4].replace('\r', '').replace('\n', '').replace(';', '')
        if re.search(r'&lt;', result[2]):
            result[2] = result[2][:re.search(r'&lt;', result[2]).start()]
        if re.search(r'&lt\/span', result[2]):
            result[2] = result[2][:re.search(r'&lt\/span', result[2]).start()]
        result[3] = re.search('Cost=.*?,', text).group()[5:-1]
        result[4] = re.search('Vps=.*?,', text).group()[4:-1]
        result[5] = re.search('Prereq=.*?&', text).group()[7:-1]
    elif occ:
        result[1] = occ.group()[4:-5]
        text = re.search(r'occ[\s\S]*forum', tmp).group()
        text2 = text[re.search(r'br&gt', text).end():]
        result[2] = text2[:re.search(r'br&gt', text2).start(
        )-4].replace('\r', '').replace('\n', '').replace(';', '')
        if re.search(r'&lt;', result[2]):
            result[2] = result[2][:re.search(r'&lt;', result[2]).start()]
        if re.search(r'&lt\/span', result[2]):
            result[2] = result[2][:re.search(r'&lt\/span', result[2]).start()]
        result[6] = re.search(r'occ-[0-9]', tmp).group()[-1]
    else:
        continue
    ans.append(result)

df = pd.DataFrame(ans, columns=['playagricolaid', 'cardname',
                                'cardtext', 'cost', 'vp', 'Prereq', 'occtype', 'Bonus', 'pass'])
df.to_csv('result2.csv')


