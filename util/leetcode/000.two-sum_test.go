package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

/*
In Go, the convention for naming test files is to use the _test.go suffix.
This is important because the Go toolchain recognizes files ending in
_test.go as test files and will execute them when you run the go test command.
*/

type args struct {
	nums   []int
	target int
}

func Test_001(t *testing.T) {
	tests := []struct {
		name string
		args args
		want []int
	}{
		{
			name: "twoSum",
			args: args{nums: []int{2, 7, 11, 15}, target: 9},
			want: []int{0, 1},
		},
		{
			name: "twoSum",
			args: args{nums: []int{3, 2, 4}, target: 6},
			want: []int{1, 2},
		},
		{
			name: "twoSum",
			args: args{nums: []int{3, 3}, target: 6},
			want: []int{0, 1},
		},
		{
			name: "twoSum",
			args: args{nums: []int{0, 4, 3, 0}, target: 0},
			want: []int{0, 3},
		},
		{
			name: "twoSum",
			args: args{nums: []int{-3, 4, 3, 90}, target: 0},
			want: []int{0, 2},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			assert.Equal(t, tt.want, twoSum(tt.args.nums, tt.args.target))
		})
	}
}
