import csv
import redis
import pandas as pd 

from itertools import zip_longest
from rich.progress import track, Progress


def batcher(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args)


def data2redis():
    redis_con = redis.Redis()

    # insert data into redis
    data_path = 'data.csv'
    data = pd.read_csv(data_path)
    data_str_list = [str(row) for row in track(data.values)]

    with Progress() as progress:
        task = progress.add_task("[cyan]Processing...", total=len(data_str_list))

        for i, data_str in enumerate(data_str_list):
            redis_con.set(f'data_{i}', data_str)
            if not redis_con.get(f'data_{i}'):
                with open('error.txt', 'a+') as f:
                    f.write(data_str + '\n')
                    
            progress.update(task, advance=1, description=f"Processing item {i}", completed=i + 1)
    progress.console.print("[green]Processing complete!")

    train_cnt = 0
    val_cnt = 0
    test_cnt = 0
    num_index = 0

    for keybatch in batcher(redis_con.scan_iter('data_*'), 500):
        for key in keybatch:
            if key is not None:
                if num_index < 2143750:
                    if redis_con.set(f'train_{train_cnt}', redis_con.get(key)):
                        redis_con.delete(key)
                        train_cnt = train_cnt + 1
                        num_index = num_index + 1
                elif 2143750 <= num_index < 2756250:
                    if redis_con.set(f'val_{val_cnt}', redis_con.get(key)):
                        redis_con.delete(key)
                        val_cnt = val_cnt + 1
                        num_index = num_index + 1
                else:
                    if redis_con.set(f'test_{test_cnt}', redis_con.get(key)):
                        redis_con.delete(key)
                        test_cnt = test_cnt + 1


def data2csv():
    redis_con = redis.Redis()
    for keybatch in batcher(redis_con.scan_iter('train_*'), 500):
        for key in keybatch:
            if key is not None:
                value = eval(redis_con.get(key).decode('utf-8').replace(' ', ','))
                with open('train_data.csv', 'a+') as file:
                    writer = csv.writer(file)
                    writer.writerow(value)

    for keybatch in batcher(redis_con.scan_iter('val_*'), 500):
        for key in keybatch:
            if key is not None:
                value = eval(redis_con.get(key).decode('utf-8').replace(' ', ','))
                with open('val_data.csv', 'a+') as file:
                    writer = csv.writer(file)
                    writer.writerow(value)

    for keybatch in batcher(redis_con.scan_iter('test_*'), 500):
        for key in keybatch:
            if key is not None:
                value = eval(redis_con.get(key).decode('utf-8').replace(' ', ','))
                with open('test_data.csv', 'a+') as file:
                    writer = csv.writer(file)
                    writer.writerow(value)


if __name__ == '__main__':
    data2csv()


