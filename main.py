#coding: utf-8

import requests
import time
import codecs
import csv
from datetime import datetime
import re

def KeyMissing(user, field):
	keys = user.keys()
	for key in keys:
		if(key == field):
			return False
	return True	

def get_posts_by_offset(user_id, offset, count, access_token, flag): 
    time.sleep(0.34)
    url = 'https://api.vk.com/method/wall.get?owner_id=-{}&offset={}&count={}&access_token={}&v=5.85'
    response = requests.get(url.format(user_id, offset, count, access_token)).json()
    print("get posts offset={}".format(offset))
    if response.get('error'):
        print(response.get('error')["error_msg"])
        return -1
    if flag == "count":
        return response[u'response']["count"]
    else:
        return response[u'response']["items"]

def csv_writer(filename, filednames, data):
    with open(filename, "w", newline='') as out_file:
        '''
        out_file - выходные данные в виде объекта
        delimiter - разделитель :|;
        fieldnames - название полей (столбцов)
        '''
        writer = csv.writer(out_file, delimiter=';')
        writer.writerow(filednames)
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    group_id = '56397759'
    token = "6c5370630c576ea066eb01b8152b7d66db088e784f2da60eec0e75d00deee66291cf74afcad858199f86a"
    fieldnames = ['date','url','text','copy_text','likes','reposts','comments','views']
    data = []
    total_posts_count = get_posts_by_offset(group_id, 0, 0, token, 'count')
    posts_count = 0
    offset = 0
    while posts_count < total_posts_count:
        posts = get_posts_by_offset(group_id, offset, 50, token, '')
        offset += 50
        for item in posts:
            post_data = []
            post_data.append(datetime.fromtimestamp(item['date']).strftime('%Y-%m-%d %H:%M:%S'))
            post_data.append('https://vk.com/overhear_tsu?w=wall-56397759_{}'.format(str(item['id'])))
            text = re.sub(r'\n','',item['text'])
            post_data.append(text)   
            if KeyMissing(item, 'copy_history') == False:
                copy_text = re.sub(r'\n','',item['copy_history'][0]['text'])
                post_data.append(copy_text)
            else:
                post_data.append('')
            post_data.append(str(item['likes']['count']))
            post_data.append(str(item['reposts']['count']))
            post_data.append(str(item['comments']['count']))
            if KeyMissing(item, 'views') == False:
                post_data.append(str(item['views']['count']))
            else:
                post_data.append('0')
            data.append(post_data)
            posts_count += 1
    print(data)
    csv_writer('data_{}.csv'.format(group_id), fieldnames, data)