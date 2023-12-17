import sys
from colorama import Fore, Style
from models import Base, Mobil
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import SCALE_nmobil,SCALE_harga,SCALE_cc,SCALE_bensin,SCALE_daya,SCALE_torsi

session = Session(engine)

def create_table():
    Base.metadata.create_all(engine)
    print(f'{Fore.GREEN}[Success]: {Style.RESET_ALL}Database has created!')

class BaseMethod():

    def __init__(self):
        # 1-5
        self.raw_weight = {'nmobil': 3, 'cc': 5, 'bensin': 3, 'daya': 3, 'torsi': 3, 'harga': 2}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k,v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(Mobil)
        return [{'id': mobil.id, 'nmobil': SCALE_nmobil[mobil.nmobil], 'cc': SCALE_cc[mobil.cc], 'bensin': SCALE_bensin[mobil.bensin], 'daya': SCALE_daya[mobil.daya], 'torsi': SCALE_torsi[mobil.torsi], 'harga': SCALE_harga[mobil.harga]} for mobil in session.scalars(query)]
    
    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        nmobils = [] # max
        ccs = [] # max
        bensins = [] # max
        dayas = [] # max
        torsis = [] # max
        hargas = [] # min
        
        for data in self.data:
            nmobils.append(data['nmobil'])
            ccs.append(data['cc'])
            bensins.append(data['bensin'])
            dayas.append(data['daya'])
            torsis.append(data['torsi'])
            hargas.append(data['harga'])
        max_nmobil = max(nmobils)
        max_cc = max(ccs)
        max_bensin = max(bensins)
        max_daya = max(dayas)
        max_torsi = max(torsis)
        min_harga = min(hargas)
        return [
            {   'id': data['id'],
                'nmobil': data['nmobil']/max_nmobil, # benefit
                'cc': data['cc']/max_cc, # benefit
                'bensin': data['bensin']/max_bensin, # benefit
                'daya': data['daya']/max_daya, # benefit
                'torsi': data['torsi']/max_torsi, # benefit
                'harga': min_harga/data['harga'] # cost
                }
            for data in self.data
        ]

class WeightedProduct(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight[WP]
        result =  {row['id']:
            round(
                row['nmobil']**weight['nmobil'] *
                row['cc']**weight['cc'] *
                row['bensin']**weight['bensin'] *
                row['daya']**weight['daya'] *
                row['torsi']**weight['torsi'] *
                row['harga']**weight['harga'],
            2)
            for row in self.normalized_data
        }
        # sorting
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))


class SimpleAdditiveWeighting(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight
        result =  {row['id']:
            round(row['nmobil'] * weight['nmobil'] +
            row['cc'] * weight['cc'] +
            row['bensin'] * weight['bensin'] +
            row['daya'] * weight['daya'] +
            row['torsi'] * weight['torsi'] +
            row['harga'] * weight['harga'], 2)
            for row in self.normalized_data
        }
        # sorting
        return dict(sorted(result.items(), key=lambda x:x[1]))

def run_saw():
    saw = SimpleAdditiveWeighting()
    print('result:', saw.calculate)

def run_wp():
    wp = WeightedProduct()
    print('result:', wp.calculate)
    pass

if len(sys.argv)>1:
    arg = sys.argv[1]

    if arg == 'create_table':
        create_table()
    elif arg == 'saw':
        run_saw()
    elif arg =='wp':
        run_wp()
    else:
        print('command not found')
