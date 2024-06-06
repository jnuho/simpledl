
# Coding test

- https://neetcode.io

- RAM: random access memory(O(1) to access)
  - store variables in byte(=8 bits) 
  - value, address stored in RAM
  - integer is 4 bytes==32 bits
    - $0, $4, $8, ... contiguous set of values (4-bytes)
  - strings
    - stored as ASCII char
    - $0, $1, $2 (1-byte)

- Static Array
  - fixed size/static (not dynamically increasing/decreasing)
  - O(1) read/write i^th element
  - O(1) insert/remove *at the end*
    - stored address is not neccessarily right after the previous array element
  - O(n) insert in the middle in worst case
    - 5, 6 (inserting 4 requres shifting in arrays)
    - 4, 5, 6
  - O(n) remove in the middle
    - 5, 6 (inserting 4 requres shifting in arrays)
    - 4, 5, 6


- Dynamic Array
  - Golang: `slice := []int{}`
  - Python: `myArr =[]`
  - Java: `List<Integer> myArr = new ArrayList<Integer>();`
  - JavaScript: `const myArr = [];`
  - C++: `vector<int> myArr;`
