import pandas as pd
import exit as exit
import dataset.dataset as dataset
import landing as landing

class Jump(landing.Landing, exit.Exit):
    def __init__(self, name, df):
        self.name = name
        self.df = dataset.Dataset(df).create()
        super().__init__(self.df)

    def get_df(self):
        return self.df

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def __str__ (self):
        return f'{self.name}'

def main():
    name = "J1"
    data = pd.read_csv(f'././data/{name}.csv', skiprows=[1])
    jump = Jump(name, data)

    jump.plt_exit()

if __name__ == "__main__":
    main()