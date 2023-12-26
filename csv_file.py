import csv
import pandas as pd
import threading

lock = threading.Lock()

# 写入多行数据
def wrows(csv_file_path, data):
    lock.acquire()
    try:
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            # 使用 writerows 方法一次性写入多行数据
            csv_writer.writerows(data)
        print("写入数据成功, 当前行数:{}".format(len(pd.read_csv(csv_file_path))))
    finally:
        lock.release()


# 追加多行数据
def arows(csv_file_path, data):
    lock.acquire()
    try:
        with open(csv_file_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            # 使用 writerows 方法一次性写入多行数据
            csv_writer.writerows(data)
        print("追加数据成功, 当前行数:{}".format(len(pd.read_csv(csv_file_path))))
    finally:
        lock.release()

# 写入一行数据
def wrow(csv_file_path, data):
    lock.acquire()
    try:
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            # 使用 writerows 方法一次性写入多行数据
            csv_writer.writerow(data)
        print("写入数据成功, 当前行数:{}".format(len(pd.read_csv(csv_file_path))))
    finally:
        lock.release()

# 追加一行数据
def arow(csv_file_path, data):
    lock.acquire()
    try:
        with open(csv_file_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            # 使用 writerows 方法一次性写入多行数据
            csv_writer.writerow(data)
        print("追加数据成功, 当前行数:{}".format(len(pd.read_csv(csv_file_path))))
    finally:
        lock.release()

# 读取文件行数
def rows_num(csv_file_path):
    return len(pd.read_csv(csv_file_path))
