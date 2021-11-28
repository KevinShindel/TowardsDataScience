import typing
import numpy as np

from rejson import Client, Path

from MemoryDataBaseUsing import REDIS_HOST, REDIS_PORT
from TrackParallelTasks.main import time_wrapper


class RedisClient:

    def __init__(self) -> None:
        self._connection = Client(host=REDIS_HOST,
                                  port=REDIS_PORT,
                                  decode_responses=True,
                                  db=0)

    @property
    def _create_pipe(self) -> Client.pipeline:
        return self._connection.pipeline()

    def set(self, key: str, data: dict) -> None:
        self._connection.jsonset(name=key, path=Path.rootPath(), obj=data)

    def get(self, key: str) -> dict:
        return {key: self._connection.jsonget(key)}

    def get_or_create(self, key: str, data: dict) -> typing.Union[(bool, dict)]:
        exist = bool(self._connection.exists(key))
        if exist:
            return exist, self.get(key=key)
        else:
            self.set(key=key, data=data)
            return exist, self.get(key=key)

    def bulk_get(self, keys: typing.List[str]) -> dict:
        pipe = self._create_pipe
        for key in keys:
            pipe.jsonget(key)
        return dict(zip(keys, pipe.execute()))

    def bulk_set(self, keys: typing.List[str], datas: typing.List[dict]) -> typing.List[bool]:
        pipe = self._create_pipe
        for key, data in zip(keys, datas):
            pipe.jsonset(key, Path.rootPath(), data)
        return pipe.execute()

    def delete(self, key):
        self._connection.delete(key)


def crud_logic():
    redis_client = RedisClient()
    data = {
        'name': "Paul",
        'Age': '25',
        'address': {
            'location': "USA"
        }
    }

    exist, instance = redis_client.get_or_create(key='employee', data=data)
    redis_client.set(key='employee', data=data)
    result = redis_client.get(key='employee')
    print(result)

    keys = [f'employee_{n}' for n in range(10)]
    redis_client.bulk_set(keys=keys, datas=[data] * 10)
    created = redis_client.bulk_get(keys)
    print(created)

    redis_client.delete('employee_1')
    created = redis_client.bulk_get(keys)
    print(created)


@time_wrapper
def bulk_set(redis, keys, data):
    redis.bulk_set(keys=keys, datas=data)


@time_wrapper
def bulk_get(redis: RedisClient, keys):
    redis.bulk_get(keys=keys)


@time_wrapper
def single_get(redis: RedisClient, keys):
    key = np.random.choice(keys)
    return redis.get(key=key)


def stress_testing():
    redis_client = RedisClient()
    MAX_COPIES = 1000000
    data = {
        'name': "Paul",
        'Age': '25',
        'address': {
            'location': "USA"
        }
    }
    keys = [f'employee_{n}' for n in range(MAX_COPIES)]
    data = [data] * MAX_COPIES

    # SET 1m copies in redis
    bulk_set(redis=redis_client, keys=keys, data=data)  # done at 47.45 sec
    bulk_get(redis=redis_client, keys=keys)  # done at 42.812 sec
    single_get(redis=redis_client, keys=keys)  # 0.208 sec

    redis_client.delete('employee_1')
    created = redis_client.bulk_get(keys)
    print(created)


def main():
    crud_logic()


if __name__ == '__main__':
    main()

