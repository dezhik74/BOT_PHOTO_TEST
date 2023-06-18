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
    Address('address1', [
        AddressWork('work1', [
            Flat('flat1'),
            Flat('flat2'),
            Flat('flat3'),
            Flat('flat4'),
        ]),
        AddressWork('work2', [
            Flat('flat1'),
            Flat('flat2'),
            Flat('flat3'),
            Flat('flat4'),
        ]),
    ]),
    Address('address2', [
        AddressWork('work1', [
            Flat('flat1'),
            Flat('flat2'),
            Flat('flat3'),
            Flat('flat4'),
            Flat('flat5'),
            Flat('flat6'),
        ]),
        AddressWork('work2', [
            Flat('flat1'),
            Flat('flat2'),
            Flat('flat3'),
            Flat('flat4'),
            Flat('flat5'),
            Flat('flat6'),
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