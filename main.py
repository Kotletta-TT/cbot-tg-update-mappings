import pandas as pd
import sys
from models import Mapping
from typing import Any, List
from db_helper import upd_db

PHONE = 0
ICCID = 1


# TODO Rename files needed?


def clean(data: Any) -> str:
    if isinstance(data, int):
        return str(data).strip()
    if isinstance(data, float):
        return str(int(data)).strip()
    else:
        return data.strip()


def get_new_mappings(filename: str, provider: str) -> List[Mapping]:
    mappings = []
    df = pd.read_excel(filename, header=None)
    phone_lst = df[PHONE].to_list()
    iccid_lst = df[ICCID].to_list()
    if len(phone_lst) != len(iccid_lst):
        raise IndexError('Length lists iccid`s and phones not exists')

    for i in range(len(iccid_lst)):
        mappings.append(Mapping(
            iccid=clean(iccid_lst[i]),
            phone=clean(phone_lst[i]),
            provider=provider))
    return mappings


def main():
    new_mappings = get_new_mappings(sys.argv[1], 'ROSTELECOM')
    upd_db(new_mappings)


if __name__ == '__main__':
    main()
