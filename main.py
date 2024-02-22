import multiprocessing
import sqlite3
import time
import concurrent.futures


connection = sqlite3.connect("./database/database.db")
cursor = connection.cursor()


def cpu_bound_ops(number):
    return sum(i * i for i in range(number))


def write_to_database(data):
    cursor.execute("BEGIN")
    try:
        cursor.execute(f"UPDATE factorials SET factorial = {data} WHERE number = 0")
        connection.commit()
    except sqlite3.DatabaseError as e:
        connection.rollback()
        print(f"Database error: {e}")


def multiprocessing_ops(numbers):
    num_processes = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(cpu_bound_ops, numbers)
        # pool.map(write_to_database, results)


def sequential_ops(numbers):
    results = [cpu_bound_ops(num) for num in numbers]
    # [write_to_database(r) for r in results]


def threading_ops(numbers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(cpu_bound_ops, numbers)
        # executor.map(write_to_database, results)


def time_it(func, *args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    duration = time.time() - start_time
    return duration


if __name__ == "__main__":
    numbers = [5_000_000 + x for x in range(20)]

    duration = time_it(multiprocessing_ops, numbers)
    print(f"Multiprocessing ops duration: {duration} seconds")

    duration = time_it(sequential_ops, numbers)
    print(f"Sequential ops duration: {duration} seconds")

    duration = time_it(threading_ops, numbers)
    print(f"Threading ops duration: {duration} seconds")

    cursor.execute("select * from factorials")
    print(cursor.fetchall())

    cursor.close()
    connection.close()
