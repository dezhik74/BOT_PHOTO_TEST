from typing import List

class Flat:
    name: str
    pk: int

    def __init__(self, name: str):
        self.name = name

class AddressWork:
    work: str
    flats: List[Flat]
    pk: int

    def __init__(self, work: str, flats: List[Flat]):
        self.work = work
        self.flats = flats

    def get_flat(self, idx) -> Flat:
        try:
            return self.flats[idx]
        except IndexError:
            return None

class Address:
    address: str
    works: List[AddressWork]
    pk: int

    def __init__(self, address: str, works: List[AddressWork]):
        self.address = address
        self.works = works

    def get_work(self, idx) -> AddressWork:
        try:
            return self.works[idx]
        except IndexError:
            return None

objects = [
    Address('Шотмана 16 к1', [
        AddressWork('ГВС', [
            Flat('Квартира 1'),
            Flat('Квартира 2'),
            Flat('Квартира 3'),
            Flat('Квартира 4'),
        ]),
        AddressWork('ХВС', [
            Flat('Квартира 1'),
            Flat('Квартира 2'),
            Flat('Квартира 3'),
            Flat('Квартира 4'),
        ]),
    ]),
    Address('Большевиков 25 к2', [
        AddressWork('ХВС', [
            Flat('Квартира 1'),
            Flat('Квартира 2'),
            Flat('Квартира 3'),
            Flat('Квартира 4'),
            Flat('Квартира 5'),
            Flat('Квартира 6'),
        ]),
        AddressWork('ТС', [
            Flat('Квартира 1'),
            Flat('Квартира 2'),
            Flat('Квартира 3'),
            Flat('Квартира 4'),
            Flat('Квартира 5'),
            Flat('Квартира 6'),
        ]),
    ]),
]

for i in range(7, 30):
    objects[1].works[1].flats.append(Flat(f"Квартира {i}"))

_adr_count = 0
for adr in objects:
    adr.pk = _adr_count
    _adr_count += 1
    _aw_count = 0
    for aw in adr.works:
        aw.address = adr
        aw.pk = _aw_count
        _aw_count += 1
        _flat_count = 0
        for flat in aw.flats:
            flat.work = aw
            flat.pk = _flat_count
            _flat_count += 1