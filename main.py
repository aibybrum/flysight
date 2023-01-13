import pandas as pd
import jsonpickle
from flysight.jump.jump import Jump


def create_jump(name):
    data = pd.read_csv(f'./data/raw/{name}.csv', skiprows=[1])
    jump = Jump(name, data)
    return jump


def safe_swoop(jump):
    my_writer_obj = open("./data/swoops.json", mode='w')
    json_data = jsonpickle.encode(jump)
    my_writer_obj.write(json_data)
    my_writer_obj.close()


def read_swoops():
    my_writer_obj = open("./data/swoops.json", mode='r')
    json_data = my_writer_obj.read()
    jmp = jsonpickle.decode(json_data)
    print(jmp)


def main():
    # safe_swoop(create_jump('J3'))
    read_swoops()


if __name__ == "__main__":
    main()
