import base64
import json
import unittest
from abc import ABC, abstractmethod
import os

HOUSE_INFO_DATA_KEY_COL = [
    "address",
    "city",
    "zip-code",
]

VERSION_NUM = 1

HOUSE_INFO_DATA_SCHEMA = {
    "version": int,
    "id": str,
    "listing_start_date": str,
    "address": str,
    "city": str,
    "zip-code": str,
    "listing_price": float,
    "type": str,
    "hoa": float,
    "fully-own": str,
    "noi": float,
    "boiler-brand": str,
    "tank-brand": str,
    "ac-brand": str,
    "roof-age": str,
    "window-age": str,
    "property-tax": float,
    "maintenance-cost": float,
    "parking-type": str,
    "inhouse-laundry": bool,
    "separate-laundry": str,
    "washer-dryer-brand": str,
    "fridge-brand": str,
    "stove-brand": str,
    "dish-washer-brand": str,
    "pets": bool,
    "year_build": int,
    "number-of-tenant": int,
    "number-of-unit": int,
    "unit-detail": str,
}


class DaoBaseException(Exception):
    pass


class HouseInfoDao:

    def __init__(self, house_info):
        self._house_info = self._initialize_house_info()
        self._generate_key()

    def _generate_key(self):
        key_col_list = []
        for i in HOUSE_INFO_DATA_KEY_COL:
            key_col_list.append(str(self._house_info[i]))

        key_col_string = ",".join(key_col_list)
        base64_key_col_string = base64.b64encode(key_col_string.encode("ascii"))
        self._key = str(base64_key_col_string, 'utf-8')
        return self._key

    def _initialize_house_info(self):
        hi = {}

        for k, _ in HOUSE_INFO_DATA_SCHEMA.items():
            hi[k] = None

        hi['version'] = VERSION_NUM
        return hi

    def contains(self, key):
        return key in self._house_info.keys()

    def get_key(self) -> str:
        return self._key

    def get_all(self) -> tuple:
        return self._key, self._house_info

    def get(self, key):
        if not self.contains(key):
            return None

        return self._house_info[key]

    def update(self, key, value):
        if not self.contains(key):
            return False

        self._house_info[key] = value
        self._generate_key()
        return True


class BasePersistStoreProvider(ABC):

    @abstractmethod
    def contains(self, info_id):
        pass

    @abstractmethod
    def add(self, info):
        pass

    @abstractmethod
    def update(self, info):
        pass

    @abstractmethod
    def delete(self, info):
        pass

    @abstractmethod
    def get(self, info_id):
        pass

    @abstractmethod
    def get_all(self):
        pass


class JsonPersistStoreProvider(BasePersistStoreProvider):
    DEFAULT_JSON_PATH = "./json_house_data.json"

    def __init__(self, json_path: str = None):
        if json_path is None:
            self._json_path = JsonPersistStoreProvider.DEFAULT_JSON_PATH
        else:
            assert isinstance(json_path, str)
            self._json_path = json_path

    def _commit(self, info_data: dict):
        json_blob = []
        for _, v in info_data.items():
            _, info_raw = v.get_all()
            json_blob.append(info_raw)

        try:
            with open('dog_breeds.txt', 'w+') as f:
                json.dump(json_blob, f)
                return True
        except Exception:
            return False

    def _fetch(self):
        info_dict = {}

        if


    def contains(self, info_id):
        pass

    def add(self, info):
        pass

    def update(self, info):
        pass

    def delete(self, info):
        pass

    def get(self, info_id):
        pass

    def get_all(self):
        pass


class HouseInfoTest(unittest.TestCase):

    def test1(self):
        h1 = {
            "address": "50-52 cedar st",
            "city": "malden",
            "zip-code": "02148",
            "type": "multi-family-2",
            "fully-own": True,
            "noi": 5000,
            "property-tax": 8679.58,
            "maintenance-cost": 1000,
            "parking-type": "driveway",
            "number-of-unit": 2,
        }

        jp = JsonPersistStoreProvider()
        h1_do = HouseInfoDao(h1)
        print(h1_do.get_all())
