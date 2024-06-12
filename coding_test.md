
# Coding test

- https://neetcode.io

- RAM: random access memory (O(1) to read/access)
  - store variables in byte(=8 bits) 
  - value, address stored in RAM
  -  random access memory; O(1) to access certain memory address
  - integer is 4 bytes==32 bits
    - $0, $4, $8, ... contiguous set of values (4-bytes)
  - strings
    - stored as ASCII char
    - $0, $1, $2 (1-byte)

- Static Array
  - fixed size/static (not dynamically increasing/decreasing)
  - O(1) read/write i^th element (due to RAM; random access memory)
  - O(1) insert/remove *at the end*
    - stored address is not neccessarily right after the previous array element
  - O(n) insert in the middle in worst case (shifting to the right takes roughly 'n' operations)
    - 5, 6 (inserting 4 requres shifting in arrays)
    - 4, 5, 6
  - O(n) remove in the middle (shift from left takes roughly 'n' operations)
    - 5, 6 (inserting 4 requres shifting in arrays)
    - 4, 5, 6


- Dynamic Array
  - Golang: `slice := make([]int, 1, 3)`
    - when allocationg more than the capacity of 3, it reallocates new memory of size 2*capacity instead of linking to old memory space
    - free the old memory of size 3, and next allocation would be 2*capacity = 12
    - inserting n elements takes O(n) : proved by power series 1+2+4+8+...
  - Python: `myArr =[]`
  - Java: `List<Integer> myArr = new ArrayList<Integer>();`
  - JavaScript: `const myArr = [];`
  - C++: `vector<int> myArr;`
  - O(1) read/write i^th element (due to RAM; random access memory)
  - O(1) insert/remove *at the end*
  - O(n) insert in the middle in worst case
  - O(n) remove in the middle


Operation           | Static Array             | Dynamic Array
--------------------|--------------------------|--------------------------
Read/Write          | O(1)                     | O(1)
Insert/Remove       | O(n)                     | Average O(1), Worst O(n)
Insert at Middle    | O(n) (copy to new array) | O(n)
Remove from Middle  | O(n) (copy to new array) | O(n)


- Stack
  - implemented using Dynamic Array
  - LIFO; Last In, First Out
  - push O(1)
  - pop O(1)
  - peek/top  O(1)

- Linked List

```go
type ListNode struct {
  Value int
  Next *ListNode
}

```



