import time
import requests
import sqlite3
from urllib.request import urlretrieve
from antigate import AntiGate

vk_api = 'https://api.vk.com/method'
vk_cfg = '&v=5.64' + '&access_token='
settings_conf = {}
tokens_list = []
names_list = []
bots_list = []


def get_settings():
    global settings_conf, tokens_list, bots_list
    try:
        file_cfg = open('settings.cfg', 'r+')
        settings_conf = [line.strip() for line in file_cfg]
        for i in range(2, len(settings_conf)):
            tokens_list.append(settings_conf[i])
            bots_list.append({'token': settings_conf[i]})
        print(f'Target link: {settings_conf[0]}')
    except FileNotFoundError:
        print('Settings file not found, please run install')
    except Exception as excp:
        print(f'Error while get settings: {excp}')


get_settings()


def verify_bots():
    global names_list
    for i in range(0, len(tokens_list)):
        try:
            r = requests.get(f'{vk_api}/account.getProfileInfo?{vk_cfg}{tokens_list[i]}').json()
            names_list.append({'name': f"{r['response']['first_name']} {r['response']['last_name']}"})
            print(f"Bot {i}: {names_list[i]['name']}")
        except:
            print(f"Bot {i}: {r['error']['error_msg']}")


verify_bots()


def get_type(target):
    try:
        target = target[target.index('vk.com/'):][7:]
        vk_resp = requests.get(f'{vk_api}/utils.resolveScreenName?screen_name={target}{vk_cfg}').json()
        _type = vk_resp['response']['type']
        _id = vk_resp['response']['object_id']
        return [_type, _id]
    except ValueError:
        print('Bad target link')
    except IndexError:
        print('Bots not found')
    except Exception as excp:
        print(f'Error while get link type: {excp}')


def get_friends(_id):
    try:
        print('Get user friends...')
        ulist = requests.get(f'{vk_api}/friends.get?order=random&user_id={_id}{vk_cfg}').json()
        return ulist['response']['items']
    except Exception as excp:
        print(f'Error while get friends: {excp}')


def get_members(_id):
    try:
        print('Get group members...')
        ulist = requests.get(f'{vk_api}/groups.getMembers?count=0&group_id={_id}{vk_cfg}').json()
        members_count = ulist['response']['count']
        if (members_count % 1000) > 0:
            reqs_nums = (members_count / 1000) + 1
        else:
            reqs_nums = members_count / 1000
        target_ulist = []
        for i in range(0, int(reqs_nums)):
            ulist = requests.get(f'{vk_api}/groups.getMembers?offset={i*1000}&group_id={_id}{vk_cfg}').json()
            target_ulist += (ulist['response']['items'])
            time.sleep(0.1)
        return target_ulist
    except Exception as excp:
        print(f'Error while get members: {excp}')


# get_type('https://vk.com/worket')


def get_used_ids(token):
    data = sqlite3.connect('data.db')
    c = data.cursor()
    t = (token,)
    c.execute("select id from requests where token=?", t)
    used_ids = []
    for row in c.execute("select id from requests where token='aaa'"):
        used_ids.append(row[0])
    data.commit()
    data.close()
    return used_ids


def get_target_ids(token, ids):
    target_ids = ids
    for i in ids:
        for j in get_used_ids(token):
            if i == j:
                target_ids.remove(i)
    return target_ids


def send_request(token, ids, name):
    for _id in ids:
        req = f'{vk_api}/friends.add?user_id={_id}{vk_cfg}{token}'
        vk_req = requests.get(req).json()
        print(f'{name}: send request to friends for id: {_id}')
        print(f'{vk_req}')
        if 'error' in vk_req:
            if vk_req['error']['error_code'] == 14:
                print('Captcha needed, request to anti-captcha.com...')
                urlretrieve(vk_req['error']['captcha_img'], 'captcha.jpg')
                captcha_key = AntiGate('d92e4ba5cd6971511b017cc0bd70abaa', 'captcha.jpg')
                vk_req = requests.get(f"{req}&captcha_sid={vk_req['error']['captcha_sid']}&captcha_key={captcha_key}").json()
                print(f'After captcha: {vk_req}')
        time.sleep(10)

for i in range(len(tokens_list)):
    try:
        type_id = get_type(settings_conf[0])
        if type_id[0] == 'user':
            list_ids = get_friends(type_id[1])
        elif type_id[0] == 'group':
            list_ids = get_members(type_id[1])
        send_request(tokens_list[i], get_target_ids(settings_conf[1], list_ids), names_list[i])
    except TypeError:
        print('Error while get target link type')
