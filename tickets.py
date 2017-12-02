#conding:utf-8

"""命令行火車票查看器

Usage:
	tickets <from> <to> <date>

"""

from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable
from colorama import Fore

class TrainsCollection:

    header='车次 车站 时间 历时 商务特等座 一等 二等 高级软卧 软卧 动卧 硬卧 软座 硬座 无座'.split()

    def __init__(self,available_trains,available_place):
        self.available_trains=available_trains
        self.available_place=available_place

    @property
    def trains(self):
        for raw_train in self.available_trains:
            raw_train_list=raw_train.split('|')
            train_no=raw_train_list[3]
            duration=raw_train_list[10]
            train=[
                train_no,
                '\n'.join([Fore.LIGHTGREEN_EX+self.available_place[raw_train_list[6]]+Fore.RESET, #station
                        Fore.LIGHTRED_EX+self.available_place[raw_train_list[7]]+Fore.RESET]),
                '\n'.join([Fore.LIGHTGREEN_EX+raw_train_list[8]+Fore.RESET,     #time
                         Fore.LIGHTRED_EX+raw_train_list[9]+Fore.RESET]),
                    duration,
                    raw_train_list[-4] if raw_train_list[-4] else '--',
                    raw_train_list[-5] if raw_train_list[-5] else '--',
                    raw_train_list[-6] if raw_train_list[-6] else '--',
                    raw_train_list[-15] if raw_train_list[-15] else '--',
                    raw_train_list[-13] if raw_train_list[-13] else '--',
                    raw_train_list[-3] if raw_train_list[-3] else '--',
                    raw_train_list[-8] if raw_train_list[-8] else '--',
                    raw_train_list[-12] if raw_train_list[-12] else '--',
                    raw_train_list[-7] if raw_train_list[-7] else '--',
                    raw_train_list[-10] if raw_train_list[-10] else '--',
                    ]
            yield train

    def pretty_print(self):
        pt=PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def cli():
    arguments=docopt(__doc__)
    from_station=stations().get(arguments['<from>'])
    to_station=stations().get(arguments['<to>'])
    date=arguments['<date>']

    url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&' \
        'leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,from_station,to_station)

    r=requests.get(url,verify=False)
    available_trans=r.json()['data']['result']
    available_place=r.json()['data']['map']

    TrainsCollection(available_trans,available_place).pretty_print()

if __name__=='__main__':
    cli()