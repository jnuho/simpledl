package main

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

/**
 You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example 1:
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]

Explanation: 342 + 465 = 807.
Example 2:
Input: l1 = [0], l2 = [0]
Output: [0]

Example 3:
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]

Constraints:
The number of nodes in each linked list is in the range [1, 100].
0 <= Node.val <= 9
It is guaranteed that the list represents a number that does not have leading zeros.
*/

/**
2->4->3
5->6->4
---
7->0->8
*/

func createListNode(n int) *ListNode {
	head := &ListNode{}
	current := head
	for n > 0 {
		// Val
		current.Val = n % 10
		if n/10 > 0 {
			current.Next = &ListNode{Val: n / 10}
		}
		current = current.Next
		n = n / 10
	}
	return head
}

func printListNode(l *ListNode) {
	result := 0
	cnt := 1

	current := l
	for current != nil {
		result += current.Val * cnt
		current = current.Next
		cnt *= 10
	}
	fmt.Println(result)
}

func Test_002(t *testing.T) {
	tests := []struct {
		name string
		l1   *ListNode
		l2   *ListNode
		want *ListNode
	}{
		{
			name: "both empty",
			l1:   nil,
			l2:   nil,
			want: nil,
		},
		{
			name: "first empty",
			l1:   nil,
			l2:   createListNode(21),
			want: createListNode(21),
		},
		{
			name: "second empty",
			l1:   createListNode(21),
			l2:   nil,
			want: createListNode(21),
		},
		{
			name: "no carry",
			l1:   createListNode(42),
			l2:   createListNode(63),
			want: createListNode(105),
		},
		{
			name: "with carry",
			l1:   createListNode(85),
			l2:   createListNode(97),
			want: createListNode(182),
		},
		{
			name: "example1",
			l1:   createListNode(342),
			l2:   createListNode(465),
			want: createListNode(807),
		},
		{
			name: "example2",
			l1:   createListNode(0),
			l2:   createListNode(0),
			want: createListNode(0),
		},
		{
			name: "example3",
			l1:   createListNode(9999999),
			l2:   createListNode(9999),
			want: createListNode(10009998),
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			assert.Equal(t, tt.want, addTwoNumbers(tt.l1, tt.l2))
		})
	}
}
