import pandas as pd
import jump.jump as jump

def main():
    name = "J1"
    data = pd.read_csv(f'././data/{name}.csv', skiprows=[1])
    jmp = jump.Jump(name, data)

    jmp.plt_exit()

if __name__ == "__main__":
    main()