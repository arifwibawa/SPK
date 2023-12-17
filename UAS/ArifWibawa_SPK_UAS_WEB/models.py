import numpy as np
import pandas as pd
from spk_model import WeightedProduct

class Mobil():

    def __init__(self) -> None:
        self.mobil = pd.read_csv('data/Arif_Wibawa_Mobil.csv')
        self.mobils = np.array(self.mobil)

    @property
    def mobil_data(self):
        data = []
        for mobil in self.mobils:
            data.append({'id': mobil[0], 'nama': mobil[1]})
        return data

    @property
    def mobil_data_dict(self):
        data = {}
        for smartphone in self.mobils:
            data[smartphone[0]] = smartphone[1] 
        return data

    def get_recs(self, kriteria:dict):
        wp = WeightedProduct(self.mobil.to_dict(orient="records"), kriteria)
        return wp.calculate

