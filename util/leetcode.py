# %%

def twoSum(nums: List[int], target: int) -> List[int]:

    """
    Finds two numbers in `nums` such that they add up to `target` and returns their indices.

    Parameters:
    nums (List[int]): A list of integers.
    target (int): The target sum.

    Returns:
    List[int]: A list containing the indices of the two numbers that add up to `target`.
                If no such pair exists, returns an empty list.
    """
    lookup = {}
    for i, num in enumerate(nums):
        if target - num in lookup:
            return [lookup[target - num], i]
        lookup[num] = i
    return []


print(twoSum([2,7,11,15], 9))