from pywebio.input import * 
from pywebio.output import *
from pywebio import session 
import requests
import http.client
from pywebio import start_server
from pywebio.session import run_js
import os


def is_valid_ipv4_address(address):
        if (address.count('.') == 3) and (''.join(address.split('.'))).isdigit():
            for i in list(map(int, address.split('.'))):
                if i > 255:
                    return True
            return False
        else:
            return True

def get_info_by_ip(ip):
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        
        data = {
            '[IP]': response.get('query'),
            '[Int prov]': response.get('isp'),
            '[Org]': response.get('org'),
            '[Country]': response.get('country'),
            '[Region Name]': response.get('regionName'),
            '[City]': response.get('city'),
            '[ZIP]': response.get('zip'),
            '[Lat]': response.get('lat'),
            '[Lon]': response.get('lon'),
        }
        
        put_table([
    [span('Информация 🌐', col=2)],
    ['IP', data['[IP]']],
    ['Интернет провайдер', data['[Int prov]']],
    ['Страна', data['[Country]']],
    ['Город', data['[Region Name]']],
    ['Почтовый индекс', data['[ZIP]']],
    ])

        put_button("🚀 Перезагрузить", onclick=lambda: run_js('window.location.reload()'))

    except requests.exceptions.ConnectionError:
        print('[!] Please check your connection!')

def main():
    info = input_group('IP CHECKER 11 📌', [
        input('🔎 Введите нужный IP-адресс:', name='ip'),
        actions('', [
            {'label': 'Отправить', 'value': 'send'},
            {'label': 'Свой IP', 'value': 'get_ip', 'color': 'warning'},
        ], name='action'),
    ], validate = lambda val: ('ip', "Введите корректный Ip адресс!") if (val["action"] == "send") and (is_valid_ipv4_address(val['ip'])) else None)
    
    if info['action'] == 'send':
        get_info_by_ip(ip=info['ip'])
    else:
        conn = session.info.user_ip
        conn = http.client.HTTPConnection("ifconfig.me")
        conn.request("GET", "/ip")
        get_info_by_ip(ip=str(conn.getresponse().read())[2:-1])

if __name__ == '__main__':
    start_server(main, debug=True, port=8080, remote_access=True)