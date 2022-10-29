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
    "listing-start-date": str,
    "address": str,
    "city": str,
    "zip-code": str,
    "listing-price": float,
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
    "in-unit-laundry": bool,
    "separate-laundry": str,
    "washer-dryer-brand": str,
    "fridge-brand": str,
    "stove-brand": str,
    "dish-washer-brand": str,
    "pets": bool,
    "year-build": int,
    "number-of-tenant": int,
    "number-of-unit": int,
    "unit-detail": str,
}


class DaoBaseException(Exception):
    pass


class BaseDao:

    @abstractmethod
    def contains(self, key) -> bool:
        pass

    @abstractmethod
    def get_key(self) -> str:
        pass

    @abstractmethod
    def get_all(self) -> tuple:
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def update(self, key, value) -> bool:
        pass


class HouseInfoDao(BaseDao):

    def __init__(self, house_info):
        self._house_info = self._initialize_house_info()
        for k, v in house_info.items():
            if self.contains(k):
                self._house_info[k] = v

        self._generate_key()

    def _generate_key(self):
        key_col_list = []
        for i in HOUSE_INFO_DATA_KEY_COL:
            key_col_list.append(str(self._house_info[i]))

        key_col_string = ",".join(key_col_list)
        base64_key_col_string = base64.b64encode(key_col_string.encode("ascii"))
        self._key = str(base64_key_col_string, 'utf-8')
        self._house_info['id'] = self._key
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


class DaoFactory:

    @classmethod
    def get_do(cls, do_type, info):
        if do_type == "house-info":
            do = HouseInfoDao(info)
            return do

        return None


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

    def __init__(self, do_type, json_path: str = None):

        # TODO validate do_type
        self._do_type = do_type

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
            with open(self._json_path, 'w+') as f:
                json.dump(json_blob, f)
                return True
        except Exception:  # TODO find out what exception needed
            return False

    def _fetch(self):
        info_dict = {}

        if not os.path.exists(self._json_path):
            print(f'Json file {self._json_path} does not exist.')
            return info_dict

        try:
            with open(self._json_path, 'r+') as f:
                json_list = json.load(f)
                for i in json_list:
                    do = DaoFactory.get_do(self._do_type, i)
                    info_dict[do.get_key()] = do
                return info_dict
        except Exception:  # TODO find out what exception needed
            return {}

    def contains(self, info_id):
        info_dict = self._fetch()
        return info_id in info_dict.keys()

    def add(self, info: BaseDao):
        info_dict = self._fetch()
        if self.contains(info.get_key()):
            return False

        info_dict[info.get_key()] = info
        return self._commit(info_dict)

    def update(self, info):
        info_dict = self._fetch()
        if self.contains(info.get_key()):
            info_dict[info.get_key()] = info
            return self._commit(info_dict)

        return False

    def delete(self, info):
        info_dict = self._fetch()
        if self.contains(info.get_key()):
            del info_dict[info.get_key()]
            return self._commit(info_dict)

        return False

    def get(self, info_id):
        info_dict = self._fetch()
        if not self.contains(info_id):
            return None

        return info_dict[info_id]

    def get_all(self):
        info_dict = self._fetch()
        return info_dict


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

        jp = JsonPersistStoreProvider("house-info")
        h1_do = HouseInfoDao(h1)
        print(h1_do.get_all())

        jp.add(h1_do)

        h2 = {
            "address": "19-21 wolcott street",
            "city": "malden",
            "zip-code": "02148",
            "type": "multi-family-3",
            "fully-own": True,
            "noi": 7000,
            "listing-price": 990000,
            "property-tax": 8679.58,
            "maintenance-cost": 1200,
            "parking-type": "driveway",
            "number-of-unit": 3,
        }

        h2_dao = HouseInfoDao(h2)

        jp.add(h2_dao)
