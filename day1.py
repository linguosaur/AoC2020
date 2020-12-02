import sys

def readInput(inputFilename):
	nums = []
	with open(inputFilename) as inputfile:
		nums = list(map(int, inputfile.readlines()))

	return nums

# Part 1: find two numbers that add up to total, and output their product
def part1(nums, total):
	for i in range(len(nums)-1):
		if nums[i+1:].count(total-nums[i]) > 0:
			return nums[i]*(total-nums[i])

# Part 2: find three numbers that add up to total, and output their product
def part2(nums, total):
	for i in range(len(nums)-2):
		for j in range(i+1, len(nums)-1):
			sum_ij = nums[i] + nums[j]
			if sum_ij < total:
				if nums[j+1:].count(total-sum_ij) > 0:
					return nums[i]*nums[j]*(total-sum_ij)


nums = readInput(sys.argv[1])
total = 2020
print(part1(nums, total))
print(part2(nums, total))
