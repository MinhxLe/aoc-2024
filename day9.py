from dataclasses import dataclass
from typing import Tuple
import bisect
import copy


@dataclass(frozen=True)
class Space:
    start: int
    length: int

    def split(self, length: int) -> Tuple["Space", "Space"]:
        assert 0 < length < self.length
        return (
            Space(self.start, length),
            Space(self.start + length, self.length - length),
        )


@dataclass(frozen=True)
class File:
    id: int
    space: Space

    def checksum(self) -> int:
        id, space = self.id, self.space
        return id * sum(range(space.start, space.start + space.length))


def parse_compact_format(disk_map: str) -> Tuple[list[File], list[Space]]:
    files = []
    free_spaces = []
    file_id = 0
    offset = 0
    is_file = True
    for length in disk_map:
        length = int(length)
        if length > 0:
            space = Space(offset, length)
            offset += length
            if is_file:
                files.append(File(file_id, space))
                file_id += 1
            else:
                free_spaces.append(space)
        is_file = not is_file
    return files, free_spaces


def move_files(files: list[File], spaces: list[Space]) -> list[File]:
    while (
        len(files) > 0 and len(spaces) > 0 and files[-1].space.start >= spaces[0].start
    ):
        space = spaces.pop(0)  # allocating first available space
        file = files.pop()  # moving file from the back

        if file.space.length < space.length:
            new_file_space, new_space = space.split(file.space.length)
            bisect.insort(
                files, File(file.id, new_file_space), key=lambda x: x.space.start
            )
            bisect.insort(spaces, new_space, key=lambda x: x.start)
        elif file.space.length == space.length:
            bisect.insort(files, File(file.id, space), key=lambda x: x.space.start)
        else:
            old_file_space, _ = file.space.split(file.space.length - space.length)
            bisect.insort(
                files, File(file.id, old_file_space), key=lambda x: x.space.start
            )
            bisect.insort(files, File(file.id, space), key=lambda x: x.space.start)
    return files


def move_files_2(files: list[File], spaces: list[Space]) -> list[File]:
    final_files = []
    for file in reversed(files):  # moving right most files first
        new_file = file
        for i, space in enumerate(spaces):
            if space.start < file.space.start:
                if space.length == file.space.length:
                    spaces.pop(i)
                    new_file = File(file.id, space)
                    break
                elif space.length > file.space.length:
                    spaces.pop(i)
                    new_file_space, new_space = space.split(file.space.length)
                    new_file = File(file.id, new_file_space)
                    bisect.insort(spaces, new_space, key=lambda x: x.start)
                    break
        final_files.append(new_file)
    final_files.sort(key=lambda x: x.space.start)
    return final_files


def merge_continuous_files(files: list[File]):
    if len(files) == 0:
        return []

    output_files = []
    current_file = files[0]
    for file in files[1:]:
        if current_file.id == file.id:
            current_file = File(
                current_file.id,
                Space(
                    current_file.space.start,
                    current_file.space.length + file.space.length,
                ),
            )
        else:
            output_files.append(current_file)
            current_file = file
    output_files.append(current_file)
    return output_files


def compute_checksum(files: list[File]) -> int:
    return sum([x.checksum() for x in files])


test_compact = "2333133121414131402"
files, spaces = parse_compact_format(test_compact)
moved_files = move_files(files, spaces)
print(compute_checksum(moved_files))

with open("data/day9.txt") as f:
    full_compact = f.read().strip()
files, spaces = parse_compact_format(full_compact)
moved_files = move_files(files, spaces)
print(compute_checksum(moved_files))


files, spaces = parse_compact_format(test_compact)
moved_files = move_files_2(files, spaces)
print(compute_checksum(moved_files))

files, spaces = parse_compact_format(compact)
moved_files = move_files_2(files, spaces)
print(compute_checksum(moved_files))
