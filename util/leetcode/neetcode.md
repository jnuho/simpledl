
# Coding test

- https://neetcode.io

## RAM: random access memory (O(1) to read/access)

- store variables in byte(=8 bits) 
- value, address stored in RAM
-    random access memory; O(1) to access certain memory address
- integer is 4 bytes==32 bits
    - $0, $4, $8, ... contiguous set of values (4-bytes)
- strings
    - stored as ASCII char
    - $0, $1, $2 (1-byte)
- golang slice
    - Both arrays and slices use direct addressing to access elements, which is why element access is O(1).
    - This is a fundamental property of RAM, where any location can be accessed directly if its address is known.

## Static Array

- fixed size/static (not dynamically increasing/decreasing)
- O(1) read/write i^th element (due to RAM; random access memory)
    - `address_of_element = base_address + (index * element_size)`
- O(1) insert/remove *at the end*
    - stored address is not neccessarily right after the previous array element
- O(n) insert in the middle in worst case (shifting to the right takes roughly 'n' operations)
    - 5, 6 (inserting 4 requres shifting in arrays)
    - 4, 5, 6
- O(n) remove in the middle (shift from left takes roughly 'n' operations)
    - 5, 6 (inserting 4 requres shifting in arrays)
    - 4, 5, 6


## Dynamic Array

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
Insert/Remove end   | O(1)                     | O(1)
Insert/Remove Middle| O(n)                     | O(n)


## Stack

- implemented using Dynamic Array
- LIFO; Last In, First Out
- push O(1)
- pop O(1)
- peek/top    O(1)

## Linked list

- O(n) to access random element

### Singly Linked List
    - pointer: reference to objects
    - order in memory(address) doesn't have to be consequent
    - but the pointer will make connections
    - L1 -> L2 -> L3, but in memory it could be L2, L1, L3

```go
type ListNode struct {
    Value int
    Next *ListNode
}

// at first head == tail
// Append at the end O(1)
//  tail.next = ListNode4
//  tail = ListNode4 // or tail = tail.Next
// Remove
//  O(n) ListNode2(change head.next=head.next.next)-> gc deletes from memory
func main() {
    l1 := &ListNode{}
    l2 := &ListNode{}
    l3 := &ListNode{}
    cur := l1
    
    // O(n)
    for cur != nil {
        cur = cur.Next
    }
}
```


### Doubly Linked List

```go
type ListNode struct {
    Value int
    Next *ListNode
    Prev *ListNode
}

// Append O(1)
//  tail.next = ListNode4
//  ListNode4.prev = tail
//  tail = tail.next
// Remove O(n)
//  node2 = tail.prev
//  node2.next=nil
//  tail = tail.prev
//  gc deletes ListNode3
func main() {
    l1 := &ListNode{}
    l2 := &ListNode{}
    l3 := &ListNode{}
    cur := l1
    
    // O(n)
    for cur != nil {
        cur = cur.Next
    }
}
```

- In general Arrays are much more efficient

Operation                  | Array   | LinkedList
---------------------------|---------|------------
Read/Write i^th            | O(1)    | O(n)
Insert/Remove end          | O(1)    | O(1)
Insert/remove at Middle    | O(n)    | O(1)


## Queues

- First in, First out (FIFO)
    - Enqueue (push): O(1)
    - Dequeue (remove): O(1)
        - advantages over array(O(n) to delete first element and shift elements)
    - Linked list (with head & tail pointer) can be used to implement queue



## Recursion

- One-Branch recursion
    - Base case (e.g. n<=1) + General case(n>1)
    - O(n)

```go
// 5! = 5 * (4*3*2*1) = 5 * factorial(5-1)
func factorial(n int) {
    if n <= 1 {
        return n
    }
    else {
        return n* factorial(n-1)
    }
}
```

- but using recursion, memory allocation is also O(n); expensive
- save factorial() function calls for all 5 steps

```go
res := 1
while n>1 {
    res = res *n
    n -=1
}
```

- Two-Branch recursion
    - Fibonacci number: F(n) = F(n-1) + F(n-2)
    - F(0) = 0, F(1) = 1
    - F(5) = F(4) + F(3)
        - F(4) = F(3) + F(2) ...
        - F(3) = F(2) + F(1) ...
    - O(2^n)

```go
func fib(n int) int {
    if n <=1 {
        return n
    }

    return fib(n-1) + fib(n-2)
}
```

## Sorting

### insertion sort
    - sub-problem of sorting first 1, first 2, ... first n elements
    - loop through the array, shifting pointer from left to right
    - [2, 3, 4, 1, 6]
    - Stable Sorting : 7-1, 3, 7-2 -> 3, 7-1, 7-2
    - Unstable Sorting : 7-1, 3, 7-2 -> 3, 7-2, 7-1
    - O(n): insertion sort on an already sorted array
    - O(n^2): insertion sort on a reversed array

```go
// Stable insertion sorting
arr := []int{2, 3, 4, 1, 6}
for i := range len(arr) {
    j := i-1
    for j >=0 && arr[j+1] < arr[j]{
        tmp := arr[j+1]
        arr[j+1] = arr[j]
        arr[j] = tmp
        j--
    }
}
```

### Merge Sort

- common and efficient