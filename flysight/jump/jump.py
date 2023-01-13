import pandas as pd

from flysight.dataset.dataset import Dataset
from flysight.jump.landing.landing import Landing
from flysight.jump.exit.exit import Exit


class Jump(Landing, Exit):
    def __init__(self, name, df):
        self.name = name
        self.df = Dataset(df).create()
        super().__init__(self.df)

    def get_df(self):
        return self.df

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return f'{self.df}'


def main():
    name = "J1"
    data = pd.read_csv(f'./../../data/raw/{name}.csv', skiprows=[1])
    jump = Jump(name, data)

    jump.plt_exit_point()
    jump.plt_exit()
    jump.plt_landing_point()


if __name__ == "__main__":
    main()
