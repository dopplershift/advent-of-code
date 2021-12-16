from __future__ import annotations

from dataclasses import dataclass
import functools

from aoc_tools import grouper


@dataclass
class Packet:
    version: int
    typ: int
    val: int | list[Packet]

    @classmethod
    def from_file(cls, fobj):
        version = fobj.read_bits(3)
        typ = fobj.read_bits(3)
        if typ == 4:
            val = 0
            while True:
                bits = fobj.read_bits(5)
                val = (val << 4) | (bits & 0xf)
                if not bits & 0x10:
                    break
            return cls(version, typ, val)
        else:
            # Operator
            if fobj.read_bits(1):
                num_packets = fobj.read_bits(11)
                subs = [Packet.from_file(fobj) for _ in range(num_packets)]
            else:
                num_bits = fobj.read_bits(15)
                start = fobj.bit_offset
                subs = []
                while fobj.bit_offset < start + num_bits:
                    subs.append(Packet.from_file(fobj))

            return cls(version, typ, subs)

    @classmethod
    def from_string(cls, s):
        return cls.from_file(BitReader(s))

    @property
    def total_version(self):
        return self.version + (0 if self.typ == 4 else sum(p.total_version for p in self.val))

    @property
    def value(self):
        match self.typ:
            case 0:
                return sum(p.value for p in self.val)
            case 1:
                return functools.reduce(lambda prod, p: prod * p.value, self.val, 1)
            case 2:
                return min(p.value for p in self.val)
            case 3:
                return max(p.value for p in self.val)
            case 4:
                return self.val
            case 5:
                return int(self.val[0].value > self.val[1].value)
            case 6:
                return int(self.val[0].value < self.val[1].value)
            case 7:
                return int(self.val[0].value == self.val[1].value)
            case _:
                raise NotImplementedError(f'Unknown packet type {self.typ}')


class BitReader:
    def __init__(self, s, chunk_size=64):
        self.chunk_size = (chunk_size // 4) * 4
        self.bit_buffer = 0
        self.bits_left = 0
        self.bit_offset = 0
        self.buffer = map(lambda a: int(''.join(a), 16),
                          grouper(s, self.chunk_size // 4, '0'))

    def ensure_bits(self, bits):
        while bits > self.bits_left:
            self.bit_buffer = (self.bit_buffer << self.chunk_size) | next(self.buffer)
            self.bits_left += self.chunk_size

    def read_bits(self, bits):
        self.ensure_bits(bits)
        self.bit_offset += bits

        # Grab as much as we need to return
        self.bits_left -= bits
        ret = self.bit_buffer >> self.bits_left

        # Keep only what hasn't been used
        self.bit_buffer &= (2 ** self.bits_left - 1)

        return ret


def run(data):
    packet = Packet.from_string(data)
    return packet.total_version, packet.value

if __name__ == '__main__':
    from aocd.models import Puzzle

    fobj = BitReader('38006F45291200')
    fobj.read_bits(3)
    assert fobj.bit_offset == 3
    fobj.read_bits(8)
    assert fobj.bit_offset == 11
    fobj.read_bits(25)
    assert fobj.bit_offset == 36

    p = Packet.from_string('D2FE28')
    assert p.version == 6
    assert p.typ == 4
    assert p.val == 2021

    p = Packet.from_string('38006F45291200')
    assert p.version == 1
    assert p.typ == 6
    assert len(p.val) == 2
    assert p.val[0].val == 10
    assert p.val[1].val == 20

    p = Packet.from_string('EE00D40C823060')
    assert p.version == 7
    assert p.typ == 3
    assert len(p.val) == 3
    assert p.val[0].val == 1
    assert p.val[1].val == 2
    assert p.val[2].val == 3

    assert Packet.from_string('8A004A801A8002F478').total_version == 16
    assert Packet.from_string('620080001611562C8802118E34').total_version == 12
    assert Packet.from_string('C0015000016115A2E0802F182340').total_version == 23
    assert Packet.from_string('A0016C880162017C3686B18A3D4780').total_version == 31

    assert Packet.from_string('C200B40A82').value == 3
    assert Packet.from_string('04005AC33890').value == 54
    assert Packet.from_string('880086C3E88112').value == 7
    assert Packet.from_string('CE00C43D881120').value == 9
    assert Packet.from_string('D8005AC2A8F0').value == 1
    assert Packet.from_string('F600BC2D8F').value == 0
    assert Packet.from_string('9C005AC2F8F0').value == 0
    assert Packet.from_string('9C0141080250320F1802104A08').value == 1

    test_a, _ = run('A0016C880162017C3686B18A3D4780')
    assert test_a == 31
    _, test_b = run('9C0141080250320F1802104A08')
    assert test_b == 1

    puz = Puzzle(2021, 16)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
