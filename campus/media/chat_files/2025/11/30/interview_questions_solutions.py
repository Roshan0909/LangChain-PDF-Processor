"""
🔢 ARRAY-BASED INTERVIEW QUESTIONS
🔤 STRING-BASED INTERVIEW QUESTIONS
🔁 SUBARRAY-SPECIFIC INTERVIEW QUESTIONS
🧩 SUBSTRING-SPECIFIC INTERVIEW QUESTIONS

Complete Python solutions with explanations and examples
"""

# ================================
# 🔢 ARRAY-BASED INTERVIEW QUESTIONS
# ================================

print("🔢 ARRAY-BASED INTERVIEW QUESTIONS")
print("=" * 50)

# 🟢 EASY QUESTIONS
print("\n🟢 EASY QUESTIONS")
print("-" * 30)

# 1. Find the maximum element in an array
def find_max_element(arr):
    """
    Find the maximum element in an array
    Time Complexity: O(n), Space Complexity: O(1)
    """
    if not arr:
        return None
    
    max_element = arr[0]
    for num in arr[1:]:
        if num > max_element:
            max_element = num
    return max_element

# Example and test
arr1 = [3, 7, 2, 9, 1, 5]
print(f"Array: {arr1}")
print(f"Maximum element: {find_max_element(arr1)}")
print()

# 2. Reverse an array in-place
def reverse_array_inplace(arr):
    """
    Reverse an array in-place using two pointers
    Time Complexity: O(n), Space Complexity: O(1)
    """
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr

# Example and test
arr2 = [1, 2, 3, 4, 5]
print(f"Original array: {arr2}")
reversed_arr = reverse_array_inplace(arr2.copy())
print(f"Reversed array: {reversed_arr}")
print()

# 3. Remove duplicates from a sorted array
def remove_duplicates_sorted(arr):
    """
    Remove duplicates from a sorted array (modify in-place)
    Time Complexity: O(n), Space Complexity: O(1)
    """
    if not arr:
        return 0
    
    unique_index = 0
    for i in range(1, len(arr)):
        if arr[i] != arr[unique_index]:
            unique_index += 1
            arr[unique_index] = arr[i]
    
    return unique_index + 1

# Example and test
arr3 = [1, 1, 2, 2, 3, 4, 4, 5]
print(f"Original sorted array: {arr3}")
length = remove_duplicates_sorted(arr3)
print(f"Array after removing duplicates: {arr3[:length]}")
print(f"New length: {length}")
print()

# 4. Find the missing number from 1 to n
def find_missing_number(arr, n):
    """
    Find missing number from 1 to n using sum formula
    Time Complexity: O(n), Space Complexity: O(1)
    """
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(arr)
    return expected_sum - actual_sum

# Example and test
arr4 = [1, 2, 4, 5, 6]  # Missing 3
n = 6
print(f"Array: {arr4}")
print(f"Missing number from 1 to {n}: {find_missing_number(arr4, n)}")
print()

# 5. Check if the array is sorted
def is_sorted(arr):
    """
    Check if array is sorted in ascending order
    Time Complexity: O(n), Space Complexity: O(1)
    """
    for i in range(1, len(arr)):
        if arr[i] < arr[i-1]:
            return False
    return True

# Example and test
arr5_sorted = [1, 2, 3, 4, 5]
arr5_unsorted = [1, 3, 2, 4, 5]
print(f"Array {arr5_sorted} is sorted: {is_sorted(arr5_sorted)}")
print(f"Array {arr5_unsorted} is sorted: {is_sorted(arr5_unsorted)}")
print()

# 🟡 MEDIUM QUESTIONS
print("🟡 MEDIUM QUESTIONS")
print("-" * 30)

# 1. Kadane's Algorithm (Maximum sum subarray)
def kadane_algorithm(arr):
    """
    Find maximum sum subarray using Kadane's algorithm
    Time Complexity: O(n), Space Complexity: O(1)
    """
    if not arr:
        return 0
    
    max_sum = current_sum = arr[0]
    start = end = temp_start = 0
    
    for i in range(1, len(arr)):
        if current_sum < 0:
            current_sum = arr[i]
            temp_start = i
        else:
            current_sum += arr[i]
        
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, (start, end)

# Example and test
arr6 = [-2, -3, 4, -1, -2, 1, 5, -3]
max_sum, indices = kadane_algorithm(arr6)
print(f"Array: {arr6}")
print(f"Maximum sum subarray: {max_sum}")
print(f"Subarray indices: {indices}")
print(f"Subarray: {arr6[indices[0]:indices[1]+1]}")
print()

# 2. Two Sum (Find two numbers that add up to target)
def two_sum(arr, target):
    """
    Find two numbers that add up to target using hash map
    Time Complexity: O(n), Space Complexity: O(n)
    """
    num_map = {}
    
    for i, num in enumerate(arr):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    
    return []

# Example and test
arr7 = [2, 7, 11, 15]
target = 9
result = two_sum(arr7, target)
print(f"Array: {arr7}")
print(f"Target: {target}")
print(f"Two sum indices: {result}")
if result:
    print(f"Numbers: {arr7[result[0]]}, {arr7[result[1]]}")
print()

# 3. Move all zeroes to the end
def move_zeros_to_end(arr):
    """
    Move all zeros to the end while maintaining relative order
    Time Complexity: O(n), Space Complexity: O(1)
    """
    non_zero_index = 0
    
    # Move all non-zero elements to the beginning
    for i in range(len(arr)):
        if arr[i] != 0:
            arr[non_zero_index] = arr[i]
            non_zero_index += 1
    
    # Fill the rest with zeros
    while non_zero_index < len(arr):
        arr[non_zero_index] = 0
        non_zero_index += 1
    
    return arr

# Example and test
arr8 = [0, 1, 0, 3, 12]
print(f"Original array: {arr8}")
result = move_zeros_to_end(arr8.copy())
print(f"After moving zeros: {result}")
print()

# 4. Find duplicate in an array of size n+1
def find_duplicate(arr):
    """
    Find duplicate using Floyd's cycle detection algorithm
    Time Complexity: O(n), Space Complexity: O(1)
    """
    # Phase 1: Find intersection point
    slow = fast = arr[0]
    
    while True:
        slow = arr[slow]
        fast = arr[arr[fast]]
        if slow == fast:
            break
    
    # Phase 2: Find entrance to cycle
    slow = arr[0]
    while slow != fast:
        slow = arr[slow]
        fast = arr[fast]
    
    return slow

# Example and test
arr9 = [1, 3, 4, 2, 2]
print(f"Array: {arr9}")
print(f"Duplicate number: {find_duplicate(arr9)}")
print()

# 5. Rotate array by k positions
def rotate_array(arr, k):
    """
    Rotate array to the right by k positions
    Time Complexity: O(n), Space Complexity: O(1)
    """
    n = len(arr)
    k = k % n  # Handle k > n
    
    # Reverse entire array
    arr.reverse()
    
    # Reverse first k elements
    arr[:k] = reversed(arr[:k])
    
    # Reverse remaining elements
    arr[k:] = reversed(arr[k:])
    
    return arr

# Example and test
arr10 = [1, 2, 3, 4, 5, 6, 7]
k = 3
print(f"Original array: {arr10}")
rotated = rotate_array(arr10.copy(), k)
print(f"After rotating by {k} positions: {rotated}")
print()

# 🔴 HARD QUESTIONS
print("🔴 HARD QUESTIONS")
print("-" * 30)

# 1. Longest Consecutive Subsequence
def longest_consecutive_subsequence(arr):
    """
    Find length of longest consecutive subsequence
    Time Complexity: O(n), Space Complexity: O(n)
    """
    if not arr:
        return 0
    
    num_set = set(arr)
    max_length = 0
    
    for num in num_set:
        # Check if it's the start of a sequence
        if num - 1 not in num_set:
            current_num = num
            current_length = 1
            
            # Count consecutive numbers
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1
            
            max_length = max(max_length, current_length)
    
    return max_length

# Example and test
arr11 = [100, 4, 200, 1, 3, 2]
print(f"Array: {arr11}")
print(f"Longest consecutive subsequence length: {longest_consecutive_subsequence(arr11)}")
print()

# 2. Find the majority element (more than n/2 times)
def find_majority_element(arr):
    """
    Find majority element using Boyer-Moore voting algorithm
    Time Complexity: O(n), Space Complexity: O(1)
    """
    candidate = None
    count = 0
    
    # Phase 1: Find candidate
    for num in arr:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)
    
    # Phase 2: Verify candidate
    if arr.count(candidate) > len(arr) // 2:
        return candidate
    
    return None

# Example and test
arr12 = [2, 2, 1, 1, 1, 2, 2]
print(f"Array: {arr12}")
print(f"Majority element: {find_majority_element(arr12)}")
print()

# 3. Product of Array Except Self (no division)
def product_except_self(arr):
    """
    Calculate product of array except self without division
    Time Complexity: O(n), Space Complexity: O(1) extra space
    """
    n = len(arr)
    result = [1] * n
    
    # Left pass
    for i in range(1, n):
        result[i] = result[i-1] * arr[i-1]
    
    # Right pass
    right_product = 1
    for i in range(n-1, -1, -1):
        result[i] *= right_product
        right_product *= arr[i]
    
    return result

# Example and test
arr13 = [1, 2, 3, 4]
print(f"Array: {arr13}")
print(f"Product except self: {product_except_self(arr13)}")
print()

# 4. Subarray with given sum (Sliding Window)
def subarray_with_sum(arr, target_sum):
    """
    Find subarray with given sum using sliding window
    Time Complexity: O(n), Space Complexity: O(1)
    """
    current_sum = 0
    start = 0
    
    for end in range(len(arr)):
        current_sum += arr[end]
        
        while current_sum > target_sum and start <= end:
            current_sum -= arr[start]
            start += 1
        
        if current_sum == target_sum:
            return (start, end)
    
    return None

# Example and test
arr14 = [1, 4, 20, 3, 10, 5]
target_sum = 33
result = subarray_with_sum(arr14, target_sum)
print(f"Array: {arr14}")
print(f"Target sum: {target_sum}")
if result:
    print(f"Subarray indices: {result}")
    print(f"Subarray: {arr14[result[0]:result[1]+1]}")
else:
    print("No subarray found")
print()

# 5. Count subarrays with sum = k
def count_subarrays_with_sum_k(arr, k):
    """
    Count subarrays with sum equal to k using prefix sum
    Time Complexity: O(n), Space Complexity: O(n)
    """
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}  # Initialize with 0 sum
    
    for num in arr:
        prefix_sum += num
        
        # Check if (prefix_sum - k) exists
        if prefix_sum - k in sum_count:
            count += sum_count[prefix_sum - k]
        
        # Update sum_count
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count

# Example and test
arr15 = [1, 1, 1]
k = 2
print(f"Array: {arr15}")
print(f"Target sum: {k}")
print(f"Count of subarrays with sum {k}: {count_subarrays_with_sum_k(arr15, k)}")
print()

# ================================
# 🔁 SUBARRAY-SPECIFIC INTERVIEW QUESTIONS
# ================================

print("\n🔁 SUBARRAY-SPECIFIC INTERVIEW QUESTIONS")
print("=" * 50)

# 🟢 EASY QUESTIONS
print("\n🟢 EASY QUESTIONS")
print("-" * 30)

# 1. Print all subarrays
def print_all_subarrays(arr):
    """
    Print all possible subarrays
    Time Complexity: O(n³), Space Complexity: O(1)
    """
    n = len(arr)
    subarrays = []
    
    for i in range(n):
        for j in range(i, n):
            subarray = arr[i:j+1]
            subarrays.append(subarray)
    
    return subarrays

# Example and test
arr16 = [1, 2, 3]
subarrays = print_all_subarrays(arr16)
print(f"Array: {arr16}")
print("All subarrays:")
for i, subarray in enumerate(subarrays):
    print(f"  {i+1}: {subarray}")
print()

# 2. Count total number of subarrays
def count_total_subarrays(arr):
    """
    Count total number of subarrays
    Formula: n*(n+1)/2
    Time Complexity: O(1), Space Complexity: O(1)
    """
    n = len(arr)
    return n * (n + 1) // 2

# Example and test
arr17 = [1, 2, 3, 4]
print(f"Array: {arr17}")
print(f"Total number of subarrays: {count_total_subarrays(arr17)}")
print()

# 🟡 MEDIUM QUESTIONS
print("🟡 MEDIUM QUESTIONS")
print("-" * 30)

# 1. Find subarray with given sum (Positive numbers) – Sliding Window
def find_subarray_with_sum(arr, target_sum):
    """
    Find subarray with given sum using sliding window (positive numbers)
    Time Complexity: O(n), Space Complexity: O(1)
    """
    current_sum = 0
    start = 0
    
    for end in range(len(arr)):
        current_sum += arr[end]
        
        while current_sum > target_sum and start <= end:
            current_sum -= arr[start]
            start += 1
        
        if current_sum == target_sum:
            return arr[start:end+1]
    
    return []

# Example and test
arr18 = [1, 4, 20, 3, 10, 5]
target = 33
result = find_subarray_with_sum(arr18, target)
print(f"Array: {arr18}")
print(f"Target sum: {target}")
print(f"Subarray with sum {target}: {result}")
print()

# 2. Longest subarray with 0 sum
def longest_subarray_zero_sum(arr):
    """
    Find longest subarray with sum 0 using prefix sum
    Time Complexity: O(n), Space Complexity: O(n)
    """
    sum_index_map = {}
    max_length = 0
    prefix_sum = 0
    
    for i, num in enumerate(arr):
        prefix_sum += num
        
        if prefix_sum == 0:
            max_length = i + 1
        elif prefix_sum in sum_index_map:
            max_length = max(max_length, i - sum_index_map[prefix_sum])
        else:
            sum_index_map[prefix_sum] = i
    
    return max_length

# Example and test
arr19 = [15, -2, 2, -8, 1, 7, 10, 23]
print(f"Array: {arr19}")
print(f"Longest subarray with 0 sum length: {longest_subarray_zero_sum(arr19)}")
print()

# 3. Longest subarray with equal number of 0s and 1s
def longest_subarray_equal_0_1(arr):
    """
    Find longest subarray with equal 0s and 1s
    Time Complexity: O(n), Space Complexity: O(n)
    """
    # Convert 0s to -1s
    converted = [-1 if x == 0 else 1 for x in arr]
    
    # Now find longest subarray with sum 0
    sum_index_map = {}
    max_length = 0
    prefix_sum = 0
    
    for i, num in enumerate(converted):
        prefix_sum += num
        
        if prefix_sum == 0:
            max_length = i + 1
        elif prefix_sum in sum_index_map:
            max_length = max(max_length, i - sum_index_map[prefix_sum])
        else:
            sum_index_map[prefix_sum] = i
    
    return max_length

# Example and test
arr20 = [0, 1, 0, 0, 1, 1, 0]
print(f"Array: {arr20}")
print(f"Longest subarray with equal 0s and 1s length: {longest_subarray_equal_0_1(arr20)}")
print()

# 🔴 HARD QUESTIONS
print("🔴 HARD QUESTIONS")
print("-" * 30)

# 1. Count subarrays with sum divisible by k
def count_subarrays_divisible_by_k(arr, k):
    """
    Count subarrays with sum divisible by k
    Time Complexity: O(n), Space Complexity: O(k)
    """
    remainder_count = {0: 1}  # Initialize with remainder 0
    prefix_sum = 0
    count = 0
    
    for num in arr:
        prefix_sum += num
        remainder = prefix_sum % k
        
        # Handle negative remainders
        if remainder < 0:
            remainder += k
        
        if remainder in remainder_count:
            count += remainder_count[remainder]
        
        remainder_count[remainder] = remainder_count.get(remainder, 0) + 1
    
    return count

# Example and test
arr21 = [4, 5, 0, -2, -3, 1]
k = 5
print(f"Array: {arr21}")
print(f"k: {k}")
print(f"Count of subarrays divisible by {k}: {count_subarrays_divisible_by_k(arr21, k)}")
print()

# 2. Maximum length subarray with sum ≤ k
def max_length_subarray_sum_le_k(arr, k):
    """
    Find maximum length subarray with sum ≤ k
    Time Complexity: O(n), Space Complexity: O(1)
    """
    max_length = 0
    current_sum = 0
    start = 0
    
    for end in range(len(arr)):
        current_sum += arr[end]
        
        while current_sum > k and start <= end:
            current_sum -= arr[start]
            start += 1
        
        max_length = max(max_length, end - start + 1)
    
    return max_length

# Example and test
arr22 = [1, 2, 3, 4, 5]
k = 8
print(f"Array: {arr22}")
print(f"k: {k}")
print(f"Maximum length subarray with sum ≤ {k}: {max_length_subarray_sum_le_k(arr22, k)}")
print()

# ================================
# 🔤 STRING-BASED INTERVIEW QUESTIONS
# ================================

print("\n🔤 STRING-BASED INTERVIEW QUESTIONS")
print("=" * 50)

# 🟢 EASY QUESTIONS
print("\n🟢 EASY QUESTIONS")
print("-" * 30)

# 1. Reverse a string
def reverse_string(s):
    """
    Reverse a string using slicing
    Time Complexity: O(n), Space Complexity: O(n)
    """
    return s[::-1]

def reverse_string_inplace(s):
    """
    Reverse a string in-place (converting to list)
    Time Complexity: O(n), Space Complexity: O(n)
    """
    s_list = list(s)
    left, right = 0, len(s_list) - 1
    
    while left < right:
        s_list[left], s_list[right] = s_list[right], s_list[left]
        left += 1
        right -= 1
    
    return ''.join(s_list)

# Example and test
s1 = "hello"
print(f"Original string: '{s1}'")
print(f"Reversed (slicing): '{reverse_string(s1)}'")
print(f"Reversed (in-place): '{reverse_string_inplace(s1)}'")
print()

# 2. Check if string is palindrome
def is_palindrome(s):
    """
    Check if string is palindrome (case-insensitive, alphanumeric only)
    Time Complexity: O(n), Space Complexity: O(1)
    """
    # Clean the string
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    
    left, right = 0, len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    
    return True

# Example and test
s2 = "A man, a plan, a canal: Panama"
print(f"String: '{s2}'")
print(f"Is palindrome: {is_palindrome(s2)}")
print()

# 3. Count vowels and consonants
def count_vowels_consonants(s):
    """
    Count vowels and consonants in a string
    Time Complexity: O(n), Space Complexity: O(1)
    """
    vowels = set('aeiouAEIOU')
    vowel_count = 0
    consonant_count = 0
    
    for char in s:
        if char.isalpha():
            if char in vowels:
                vowel_count += 1
            else:
                consonant_count += 1
    
    return vowel_count, consonant_count

# Example and test
s3 = "Hello World"
vowels, consonants = count_vowels_consonants(s3)
print(f"String: '{s3}'")
print(f"Vowels: {vowels}, Consonants: {consonants}")
print()

# 4. Check anagrams of two strings
def are_anagrams(s1, s2):
    """
    Check if two strings are anagrams
    Time Complexity: O(n), Space Complexity: O(1)
    """
    # Remove spaces and convert to lowercase
    s1 = s1.replace(' ', '').lower()
    s2 = s2.replace(' ', '').lower()
    
    if len(s1) != len(s2):
        return False
    
    # Count characters
    char_count = {}
    
    for char in s1:
        char_count[char] = char_count.get(char, 0) + 1
    
    for char in s2:
        if char not in char_count:
            return False
        char_count[char] -= 1
        if char_count[char] == 0:
            del char_count[char]
    
    return len(char_count) == 0

# Example and test
s4 = "listen"
s5 = "silent"
print(f"String 1: '{s4}'")
print(f"String 2: '{s5}'")
print(f"Are anagrams: {are_anagrams(s4, s5)}")
print()

# 5. Remove all duplicates from a string
def remove_duplicates(s):
    """
    Remove all duplicate characters from string
    Time Complexity: O(n), Space Complexity: O(n)
    """
    seen = set()
    result = []
    
    for char in s:
        if char not in seen:
            seen.add(char)
            result.append(char)
    
    return ''.join(result)

# Example and test
s6 = "programming"
print(f"Original string: '{s6}'")
print(f"After removing duplicates: '{remove_duplicates(s6)}'")
print()

# 🟡 MEDIUM QUESTIONS
print("🟡 MEDIUM QUESTIONS")
print("-" * 30)

# 1. Longest common prefix
def longest_common_prefix(strs):
    """
    Find longest common prefix among strings
    Time Complexity: O(S), Space Complexity: O(1)
    where S is sum of all characters
    """
    if not strs:
        return ""
    
    prefix = strs[0]
    
    for string in strs[1:]:
        while not string.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    
    return prefix

# Example and test
strs1 = ["flower", "flow", "flight"]
print(f"Strings: {strs1}")
print(f"Longest common prefix: '{longest_common_prefix(strs1)}'")
print()

# 2. First non-repeating character
def first_non_repeating_char(s):
    """
    Find first non-repeating character
    Time Complexity: O(n), Space Complexity: O(1)
    """
    char_count = {}
    
    # Count characters
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    # Find first non-repeating
    for char in s:
        if char_count[char] == 1:
            return char
    
    return None

# Example and test
s7 = "leetcode"
print(f"String: '{s7}'")
print(f"First non-repeating character: '{first_non_repeating_char(s7)}'")
print()

# 3. Check if string can become palindrome after removing one character
def can_be_palindrome_after_removal(s):
    """
    Check if string can become palindrome after removing one character
    Time Complexity: O(n), Space Complexity: O(1)
    """
    def is_palindrome_range(s, left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True
    
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            # Try removing left character or right character
            return (is_palindrome_range(s, left + 1, right) or 
                    is_palindrome_range(s, left, right - 1))
        left += 1
        right -= 1
    
    return True

# Example and test
s8 = "abca"
print(f"String: '{s8}'")
print(f"Can become palindrome after removing one char: {can_be_palindrome_after_removal(s8)}")
print()

# 4. Group anagrams from list
def group_anagrams(strs):
    """
    Group anagrams together
    Time Complexity: O(n * k log k), Space Complexity: O(n * k)
    where n is number of strings, k is max length
    """
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        key = ''.join(sorted(s))
        anagram_groups[key].append(s)
    
    return list(anagram_groups.values())

# Example and test
strs2 = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(f"Strings: {strs2}")
print(f"Grouped anagrams: {group_anagrams(strs2)}")
print()

# 5. String compression
def string_compression(s):
    """
    Compress string (e.g., aaabbc → a3b2c1)
    Time Complexity: O(n), Space Complexity: O(n)
    """
    if not s:
        return ""
    
    result = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            result.append(current_char + str(count))
            current_char = s[i]
            count = 1
    
    # Add the last group
    result.append(current_char + str(count))
    
    return ''.join(result)

# Example and test
s9 = "aaabbc"
print(f"Original string: '{s9}'")
print(f"Compressed string: '{string_compression(s9)}'")
print()

# 🔴 HARD QUESTIONS
print("🔴 HARD QUESTIONS")
print("-" * 30)

# 1. Minimum window substring
def min_window_substring(s, t):
    """
    Find minimum window substring containing all characters of t
    Time Complexity: O(|s| + |t|), Space Complexity: O(|s| + |t|)
    """
    if not s or not t:
        return ""
    
    # Character frequency in t
    dict_t = {}
    for char in t:
        dict_t[char] = dict_t.get(char, 0) + 1
    
    required = len(dict_t)
    formed = 0
    window_counts = {}
    
    left = right = 0
    min_len = float('inf')
    min_left = 0
    
    while right < len(s):
        # Add character from right
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in dict_t and window_counts[char] == dict_t[char]:
            formed += 1
        
        # Try to shrink window from left
        while left <= right and formed == required:
            char = s[left]
            
            # Update minimum window
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            window_counts[char] -= 1
            if char in dict_t and window_counts[char] < dict_t[char]:
                formed -= 1
            
            left += 1
        
        right += 1
    
    return "" if min_len == float('inf') else s[min_left:min_left + min_len]

# Example and test
s10 = "ADOBECODEBANC"
t1 = "ABC"
print(f"String: '{s10}'")
print(f"Pattern: '{t1}'")
print(f"Minimum window substring: '{min_window_substring(s10, t1)}'")
print()

# 2. Longest Palindromic Substring
def longest_palindromic_substring(s):
    """
    Find longest palindromic substring using expand around centers
    Time Complexity: O(n²), Space Complexity: O(1)
    """
    if not s:
        return ""
    
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    start = 0
    max_len = 0
    
    for i in range(len(s)):
        # Odd length palindromes
        len1 = expand_around_center(i, i)
        # Even length palindromes
        len2 = expand_around_center(i, i + 1)
        
        current_max = max(len1, len2)
        if current_max > max_len:
            max_len = current_max
            start = i - (current_max - 1) // 2
    
    return s[start:start + max_len]

# Example and test
s11 = "babad"
print(f"String: '{s11}'")
print(f"Longest palindromic substring: '{longest_palindromic_substring(s11)}'")
print()

# 3. Edit distance between two strings
def edit_distance(s1, s2):
    """
    Calculate edit distance using dynamic programming
    Time Complexity: O(m*n), Space Complexity: O(m*n)
    """
    m, n = len(s1), len(s2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # deletion
                    dp[i][j-1],    # insertion
                    dp[i-1][j-1]   # substitution
                )
    
    return dp[m][n]

# Example and test
s12 = "horse"
s13 = "ros"
print(f"String 1: '{s12}'")
print(f"String 2: '{s13}'")
print(f"Edit distance: {edit_distance(s12, s13)}")
print()

# ================================
# 🧩 SUBSTRING-SPECIFIC INTERVIEW QUESTIONS
# ================================

print("\n🧩 SUBSTRING-SPECIFIC INTERVIEW QUESTIONS")
print("=" * 50)

# 🟢 EASY QUESTIONS
print("\n🟢 EASY QUESTIONS")
print("-" * 30)

# 1. Print all substrings
def print_all_substrings(s):
    """
    Print all possible substrings
    Time Complexity: O(n³), Space Complexity: O(1)
    """
    n = len(s)
    substrings = []
    
    for i in range(n):
        for j in range(i, n):
            substrings.append(s[i:j+1])
    
    return substrings

# Example and test
s14 = "abc"
substrings = print_all_substrings(s14)
print(f"String: '{s14}'")
print("All substrings:")
for i, substring in enumerate(substrings):
    print(f"  {i+1}: '{substring}'")
print()

# 2. Count total substrings
def count_total_substrings(s):
    """
    Count total number of substrings
    Formula: n*(n+1)/2
    Time Complexity: O(1), Space Complexity: O(1)
    """
    n = len(s)
    return n * (n + 1) // 2

# Example and test
s15 = "abcd"
print(f"String: '{s15}'")
print(f"Total number of substrings: {count_total_substrings(s15)}")
print()

# 🟡 MEDIUM QUESTIONS
print("🟡 MEDIUM QUESTIONS")
print("-" * 30)

# 1. Longest substring without repeating characters
def longest_substring_without_repeating(s):
    """
    Find longest substring without repeating characters using sliding window
    Time Complexity: O(n), Space Complexity: O(min(m,n))
    """
    char_map = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        if s[right] in char_map:
            left = max(left, char_map[s[right]] + 1)
        
        char_map[s[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Example and test
s16 = "abcabcbb"
print(f"String: '{s16}'")
print(f"Longest substring without repeating chars length: {longest_substring_without_repeating(s16)}")
print()

# 2. Check if one string is a rotation of another
def is_rotation(s1, s2):
    """
    Check if s1 is a rotation of s2
    Time Complexity: O(n), Space Complexity: O(n)
    """
    if len(s1) != len(s2):
        return False
    
    # s1 is rotation of s2 if s1 is substring of s2+s2
    return s1 in s2 + s2

# Example and test
s17 = "waterbottle"
s18 = "erbottlewat"
print(f"String 1: '{s17}'")
print(f"String 2: '{s18}'")
print(f"Is s1 rotation of s2: {is_rotation(s17, s18)}")
print()

# 3. Check if string is subsequence of another
def is_subsequence(s, t):
    """
    Check if s is subsequence of t
    Time Complexity: O(n), Space Complexity: O(1)
    """
    i = 0  # pointer for s
    
    for char in t:
        if i < len(s) and char == s[i]:
            i += 1
    
    return i == len(s)

# Example and test
s19 = "ace"
s20 = "abcde"
print(f"String s: '{s19}'")
print(f"String t: '{s20}'")
print(f"Is s subsequence of t: {is_subsequence(s19, s20)}")
print()

# 🔴 HARD QUESTIONS
print("🔴 HARD QUESTIONS")
print("-" * 30)

# 1. Count substrings with exactly k distinct characters
def count_substrings_k_distinct(s, k):
    """
    Count substrings with exactly k distinct characters
    Time Complexity: O(n²), Space Complexity: O(k)
    """
    def count_at_most_k_distinct(s, k):
        if k == 0:
            return 0
        
        count = 0
        char_count = {}
        left = 0
        
        for right in range(len(s)):
            char_count[s[right]] = char_count.get(s[right], 0) + 1
            
            while len(char_count) > k:
                char_count[s[left]] -= 1
                if char_count[s[left]] == 0:
                    del char_count[s[left]]
                left += 1
            
            count += right - left + 1
        
        return count
    
    return count_at_most_k_distinct(s, k) - count_at_most_k_distinct(s, k - 1)

# Example and test
s21 = "aba"
k = 2
print(f"String: '{s21}'")
print(f"k: {k}")
print(f"Count of substrings with exactly {k} distinct chars: {count_substrings_k_distinct(s21, k)}")
print()

# 2. Longest substring with at most k distinct characters
def longest_substring_k_distinct(s, k):
    """
    Find longest substring with at most k distinct characters
    Time Complexity: O(n), Space Complexity: O(k)
    """
    if k == 0:
        return 0
    
    char_count = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Example and test
s22 = "eceba"
k = 2
print(f"String: '{s22}'")
print(f"k: {k}")
print(f"Longest substring with at most {k} distinct chars: {longest_substring_k_distinct(s22, k)}")
print()

# 3. Count of palindromic substrings
def count_palindromic_substrings(s):
    """
    Count all palindromic substrings
    Time Complexity: O(n²), Space Complexity: O(1)
    """
    def expand_around_center(left, right):
        count = 0
        while left >= 0 and right < len(s) and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
        return count
    
    total_count = 0
    
    for i in range(len(s)):
        # Odd length palindromes
        total_count += expand_around_center(i, i)
        # Even length palindromes
        total_count += expand_around_center(i, i + 1)
    
    return total_count

# Example and test
s23 = "abc"
print(f"String: '{s23}'")
print(f"Count of palindromic substrings: {count_palindromic_substrings(s23)}")
print()

print("🎉 All interview questions solved with explanations and examples!")
print("=" * 70)
