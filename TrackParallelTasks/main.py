from concurrent.futures.thread import ThreadPoolExecutor
import os
import time
from p_tqdm import p_map, p_umap, p_imap, p_uimap
from tqdm.auto import tqdm


def time_wrapper(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Function [{func.__name__}] done at: {round(end-start, 3)} seconds')
        return result
    return wrapper


numbers = list(range(0, 10000))
CONSTANT = 1
num_cpus = os.cpu_count() * 10  # number of physical cores * multiply from x5 to x10


def heavy_processing(number):
    time.sleep(0.05)
    output = number + CONSTANT
    return output


@time_wrapper
def one_thread():
    """
    Simple processing without threading and without tdqm
    :return:
    """
    results = []
    for number in numbers:
        result = heavy_processing(number)
        results.append(result)
    return results


def one_yield_thread():
    """
    Simple processing without threading and without tdqm
    :return:
    """
    for number in numbers:
        result = heavy_processing(number)
        yield result


@time_wrapper
def tqdm_one_thread():
    """
    Simple processing without threading but with tqdm plugin
    :return:
    """
    results = []
    for number in tqdm(numbers):  # 20 it/s --> 1 core
        result = heavy_processing(number)
        results.append(result)
    return results


@time_wrapper
def tdqm_multi_thread(func):
    """
    p_map: returning a list
    p_imap: that does the same thing but instead of returning a list, returns an iterator
    p_umap`: that returns an unordered list (the processing is not especially faster)
    p_uimap: returns an iterator of unordered elements
    :return: Iterable
    """
    results = func(heavy_processing, numbers, **{"num_cpus": num_cpus})
    return results


@time_wrapper
def multi_thread_executor():
    with ThreadPoolExecutor(max_workers=num_cpus) as executor:
        result = executor.map(heavy_processing, numbers)
    return result


@time_wrapper
def calc_time(data):
    return list(data)


if __name__ == '__main__':
    # BASICAL TASKS
    one_thread()
    calc_time(one_yield_thread())
    multi_thread_executor()
    # TQDM TASKS
    tqdm_one_thread()
    tdqm_multi_thread(p_map)
    calc_time(tdqm_multi_thread(p_imap))
    tdqm_multi_thread(p_umap)
    calc_time(tdqm_multi_thread(p_uimap))
