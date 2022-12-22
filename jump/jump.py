import pandas as pd
import exit as exit
import dataset.dataset as dataset
import landing as landing

class Jump(exit.Exit, landing.Landing):
    def __init__(self, name, df):
        self.name = name
        self.df = dataset.Dataset(df).create()
        exit.Exit.__init__(self, self.df)
        landing.Landing.__init__(self, self.df)

    def get_df(self):
        return self.df

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def __str__ (self):
        return f'{self.name}'

def main():
    data = pd.read_csv('././data/J1.csv', skiprows=[1])
    jump = Jump("v1", data)
    
if __name__ == "__main__":
    main()