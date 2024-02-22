# -------------------------------------first challenge-----------------------------------------------------------
# Have the function MathChallenge(str) take the str parameter,
# which will be a simple mathematical formula with three numbers, a single operator (+, -, *, or /)
# and an equal sign (=) and return the digit that completes the equation. In one of the numbers in the equation,
# there will be an x character, and your program should determine what digit is missing. For example,
# if str is "3x + 12 = 46" then your program should output 4. The x character can appear in any of the three numbers
# and all three numbers will be greater than or equal to 0 and less than or equal to 1000000.
# Examples
# Input: "4 - 2 = x"
# Output: 2
# Input: "1x0 * 12 = 1200"
# Output: 0


# def MathChallenge(str):
#     str=str.split(' ')
#     first=str[0]
#     second=str[2]
#     operator=str[1]
#     third=str[len(str)-1]
#     print(str,first,second,operator,third)
#     if 'x' in first:
#         first = [i for i in first if i.isdigit()]
#         first = int(''.join(first))
#         if operator=='-':
#             result=int(third)+int(second)
#         elif operator=='+':
#             result=int(third)-int(second)
#         elif operator=='*':
#             result=int(third)//int(second)
#         elif operator=='/':
#             result=int(third)*int(second)
#         x=result//first
#         return x
#     elif 'x' in second:
#         second = [i for i in second if i.isdigit()]
#         second=int(''.join(second))
#         if operator == '-':
#             result = int(first) - int(third)
#         elif operator == '+':
#             result = int(first) + int(third)
#         elif operator == '*':
#             result = int(first) * int(third)
#         elif operator == '/':
#             result = int(first) // int(third)
#         x = result // second
#         return x
#     else:
#         if operator == '-':
#             result = int(first) - int(second)
#         elif operator == '+':
#             result = int(first) + int(second)
#         elif operator == '*':
#             result = int(first) * int(second)
#         elif operator == '/':
#             result = int(first) // int(second)
#         return result
#
#
# print(MathChallenge("10x - 2 = 98"))

# -----------------------------------------------------second challenge---------------------------------------------------
# Have the function ArrayChallenge(arr) take the array of numbers stored in arr and
# first determine the largest element in the array, and then determine whether or not you can reach that same element
# within the array by moving left or right continuously according to whatever integer is in the current spot.
# If you can reach the same spot within the array, then your program should output the least amount of jumps it took.
# For example: if the input is [2, 3, 5, 6, 1] you'll start at the spot where 6 is and
# if you jump 6 spaces to the right while looping around the array you end up at the last element where the 1 is.
# Then from here you jump 1 space to the left and you're back where you started, so your program should output 2.
# If it's impossible to end up back at the largest element in the array your program should output -1.
# The largest element in the array will never equal the number of elements in the array.
# The largest element will be unique.
# Examples
# Input: [1,2,3,4,2]
# Output: 3
# Input: [1,7,1,1,1,1]
# Output: 2
#
# list=[1,2,3,4,7]
# print(list.index(max(list)))


# ----------------------------------------------------Third challenge------------------------------------------------------------
# Have the function ArrayChallenge(strArr) take the array of strings stored in strArr
# and return the third largest word within it.
# So for example: if strArr is ["hello", "world", "before", "all"]
# your output should be world because "before" is 6 letters long,
# and "hello" and "world" are both 5, but the output should be world
# because it appeared as the last 5 letter word in the array.
# If strArr was ["hello", "world", "after", "all"] the output should be after
# because the first three words are all 5 letters long,
# so return the last one. The array will have at least three strings and each string will only contain letters.
# Examples
# Input: ["coder","byte","code"]
# Output: code
# Input: ["abc","defg","z","hijk"]
# Output: abc


# def Arraychallenge(str):
#     listlen = [len(i) for i in str]
#     listlen.sort(reverse=True)
#     thirdmaxlen=listlen[2]
#     str=[i for i in str if len(i)==thirdmaxlen]
#     print(str[len(str)-1])
# Arraychallenge(["abc","defg","z","hijk"])


# #----------------------------------------------- Practice-----------------------------------------
# for i in range(1,101):
#     if i%3==0 and i%5==0:
#        print('FizzBuzz')
#     elif not i % 3:
#        print('Fizz')
#     elif not i % 5:
#        print('Buzz')
#     else:
#         print(i)

# def sum(list1,s):
#     list2=[(list1[i],list1[j]) for i in range(0,len(list1)) for j in range( i+1 , len(list1)) if list1[i]+list1[j]==s]
#     if len(list2):
#         print(True)
#     else:
#         print(False)
#
# sum([1,2,3,4,5,6,7,8],11)
# import sympy
# # def remove(arr,string):
# #     list1=[i for i in string if i not in arr]
# #     print("".join(list1))
# #
# #
# # remove(['h','e','w','o'],'hello world')
# print(sympy.isprime(3))
# import datetime
#
# d = datetime.datetime.now()
# print(d)
# print(datetime.timedelta(hours=48))
# e = d - (d - datetime.timedelta(hours=48))
# print(e)
# if e.days == 1:
#     print("if")
# else:
#     print("else")

zoo=['monkey','elephant','tiger','lion','chetah']
zoo.pop(3)
print(zoo)
zoo.append('lion')
print(zoo)
del zoo[0]
print(zoo)
print(zoo[0:3])
