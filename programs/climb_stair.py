
def climb_stair(n):
    #initialize array 1 greater than n full of zeroes
    arr = [0] * (n + 1) 
    #number of ways to get to first step going by 1 or 2 is 1
    #(0->1)
    arr[1] = 1
    #number of ways to get to second step going by 1 or 2 is 2
    #(0->1->1) or (0->2)
    arr[2] = 2
    for i in range(3, len(arr)):
        #number of ways to get to ith step is i-1 + i-2 ways
        arr[i] = arr[i-1] + arr[i-2]
    #return last element of array
    return arr[-1]



if __name__ == "__main__":
    print(climb_stair(10))
    print(climb_stair(20))
    print(climb_stair(30))

