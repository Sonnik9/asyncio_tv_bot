import os
import psutil

num_cores = os.cpu_count()
print(f"Количество ядер процессора: {num_cores}")


# Загруженность процессора в процентах
cpu_usage = psutil.cpu_percent(interval=1)
print(f"Загруженность процессора: {cpu_usage}%")

# python cpu_test.py
