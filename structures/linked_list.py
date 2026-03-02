from collections.abc import Collection
from dataclasses import dataclass
from typing import Any

"""A node of a linked list. Contains data and a pointer to the next node"""


@dataclass(slots=True)  # dataclass to simplify node class and reduce memory usage
class _Node:
    data: Any
    next: "_Node | None" = None


"""A singly linked list. Provides a variety of functions for editing the list"""


class LinkedList:
    # Initializes a linked list with optional initial values in a collection.
    def __init__(self, items: Collection[Any] | None = None) -> None:
        self.list_size: int = 0
        self.head: _Node | None = None
        self.tail: _Node | None = None

        if items is not None:
            self.append_all(items)

    # Appends a value to the list at the specified index (or at the end if none is provided)
    def append(self, value: Any, index: int | None = None) -> None:
        if index is None:
            index = self.list_size

        if index < 0 or index > self.list_size:
            raise IndexError(f"Index {index} out of bounds.")

        new_node = _Node(value)

        if index == 0:
            # insert at the beginning
            new_node.next = self.head
            self.head = new_node
            if self.list_size == 0:
                self.tail = new_node
        elif index == self.list_size:
            # insert at the end
            assert self.tail is not None
            self.tail.next = new_node
            self.tail = new_node
        else:
            # insert in the middle
            prev = self.head
            for _ in range(index - 1):
                assert prev is not None
                prev = prev.next
            assert prev is not None
            new_node.next = prev.next
            prev.next = new_node

        self.list_size += 1

    # Appends a collection of values to the list at the specified index (or at the end if none is provided).
    def append_all(self, values: Collection[Any], index: int | None = None) -> None:
        if index is None:
            index = self.list_size
        for value in values:
            self.append(value, index)
            index += 1

    # Empties the contents of the list.
    def clear(self) -> None:
        self.head = None
        self.tail = None
        self.list_size = 0

    # Returns the number of items in the LinkedList
    def size(self) -> int:
        return self.list_size

    # Returns True if the list's size is 0, False otherwise.
    def is_empty(self) -> bool:
        return self.list_size == 0

    # Returns True if the LinkedList contains the specified value, False otherwise.
    def contains(self, item: Any) -> bool:
        if self.list_size == 0:
            return False

        assert self.head is not None, (
            "LinkedList corrupted. Head is None while list is not empty."
        )
        curr: _Node | None = self.head
        i: int = 0
        while curr is not None:
            if curr.data == item:
                return True
            curr = curr.next
            i += 1
        return False

    # Returns the value at a given index.
    def get(self, index: int) -> Any:
        if index < 0 or index >= self.list_size:
            raise IndexError(
                f"Index {index} out of bounds for LinkedList of length {self.size()}."
            )
        assert self.head is not None, (
            f"LinkedList corrupted while getting value at index {index}."
        )
        curr: _Node = self.head
        for i in range(index):
            assert curr.next is not None, (
                f"LinkedList corrupted while getting value at index {index}."
            )
            curr = curr.next
        return curr.data

    # Replaces the value at an index with a provided new value.
    def set(self, index: int, item: Any) -> Any:
        if index < 0 or index >= self.list_size:
            raise IndexError("Cannot set to an out of bounds index.")

        replaced: Any

        if index == 0:
            assert self.head is not None, (
                "Head was None when it shouldn't have been in method set."
            )
            replaced = self.head.data
            self.head.data = item
        elif index == self.list_size - 1:
            assert self.tail is not None, (
                "Tail was None when it shouldn't have been in method set."
            )
            replaced = self.tail.data
            self.tail.data = item
        else:
            assert self.head is not None
            current: _Node = self.head
            for i in range(index):
                assert current.next is not None
                current = current.next
            replaced = current.data
            current.data = item
        return replaced

    # Returns the index of the given value's first occurrence.
    def index_of(self, item: Any) -> int:
        if self.list_size == 0:
            return -1

        assert self.head is not None
        current: _Node | None = self.head
        i: int = 0
        while current is not None:
            if current.data is item:
                return i
            current = current.next
            i += 1
        return -1

    # Returns the index of the given value's last occurrence.
    def last_index_of(self, item: Any) -> int:
        if self.list_size == 0:
            return -1
        last_index: int = -1
        assert self.head is not None
        current = self.head
        i: int = 0
        while current is not None:
            if current.data is item:
                last_index = i
            current = current.next
            i += 1
        return last_index

    # Removes the value at a given index and returns what was removed.
    def remove_by_index(self, index: int) -> Any:
        if index < 0 or index >= self.list_size:
            raise IndexError("Cannot remove an out of bounds index.")

        removed: Any

        if self.list_size == 1:
            assert self.head is not None
            removed = self.head.data
            self.clear()
            return removed
        elif index == 0:
            assert self.head is not None
            removed = self.head.data
            self.head = self.head.next
        else:
            assert self.head is not None
            current: _Node = self.head
            for i in range(1, index):
                assert current.next is not None
                current = current.next
            assert current.next is not None
            removed = current.next.data
            if current.next == self.tail:
                self.tail = current
            current.next = current.next.next

        self.list_size -= 1
        return removed

    # Removes the first occurrence of a given value and returns True if the list actually contained it.
    def remove_by_item(self, item: Any) -> bool:
        if self.list_size == 0:
            return False

        index: int = self.index_of(item)
        if index != -1:
            self.remove_by_index(index)
            return True
        return False

    # Returns a string representation of the list in the format [1, 2, 3, 4, 5].
    def __str__(self) -> str:
        if self.list_size == 0:
            return "[]"
        result: list = ["["]
        assert self.head is not None, "LinkedList corrupted in str()"
        item: _Node = self.head
        for _ in range(self.list_size - 1):
            result.append(f"{repr(item.data)}, ")
            assert item.next is not None, "LinkedList corrupted in str()"
            item = item.next
        result.append(f"{repr(item.data)}]")
        return "".join(result)
