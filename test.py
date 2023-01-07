import pandas as pd
from flysight.jump.jump import Jump


def main():
    name = "J1"
    data = pd.read_csv(f'././data/{name}.csv', skiprows=[1])
    jmp = Jump(name, data)

    jmp.plt_exit()


if __name__ == "__main__":
    main()
