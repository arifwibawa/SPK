from settings import MEREK_SCALE,SCALE_harga,SCALE_cc,SCALE_bensin,SCALE_daya,SCALE_torsi

class BaseMethod():

    def __init__(self, data_dict, **setWeight):
        self.dataDict = data_dict

        # 1-7 (Kriteria)
        self.raw_weight = {
            'nmobil': 3, 
            'cc': 5, 
            'bensin': 3, 
            'daya': 3, 
            'torsi': 3, 
            'harga': 2
        }

        if setWeight:
            for item in setWeight.items():
                temp1 = setWeight[item[0]] # value int
                temp2 = {v: k for k, v in setWeight.items()}[item[1]] # key str

                setWeight[item[0]] = item[1]
                setWeight[temp2] = temp1

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    @property
    def data(self):
        return [{
            'id': mobil['id'],
            'nmobil': MEREK_SCALE[mobil['nmobil']],
            'cc': SCALE_cc[mobil['cc']],
            'bensin': SCALE_bensin[mobil['bensin']],
            'daya': SCALE_daya[mobil['daya']],
            'torsi': SCALE_torsi[mobil['torsi']],
            'harga': SCALE_harga[mobil['harga']]
        } for mobil in self.dataDict]
    
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
    def __init__(self, dataDict, setWeight:dict):
        super().__init__(data_dict=dataDict, **setWeight)
    @property
    def calculate(self):
        weight = self.weight
        result = {row['id']:
    round(
        row['nmobil'] ** weight['nmobil'] *
        row['cc'] ** weight['cc'] *
        row['bensin'] ** weight['bensin'] *
        row['daya'] ** weight['daya'] *
        row['torsi'] ** weight['torsi'] *
        row['harga'] ** weight['harga']
        , 2
    )
    for row in self.normalized_data}

        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))