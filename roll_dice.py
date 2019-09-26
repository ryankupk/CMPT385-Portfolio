def roll_dice(N,M):
    arr = [[0] * (M + 1) for i in range(N + 1)]
    #initialize (0, 0) with 1 so that it can be added for the first row
    arr[0][0] = 1
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            #you can not roll a number less than the number of dice that you have
            if j < i:
                arr[i][j] = 0
            #you can not roll more than 6 * the number of dice that you have
            elif j > 6 * i:
                arr[i][j] = 0
            else:
                #the number of ways to roll M with N dice is equal to the number of ways to roll the sum of (M-6) through (M-1) inclusive with (N-1) die
                for k in range(6, 0, -1):
                    if j >= k:
                            arr[i][j] += arr[i-1][j-k]
            
    return arr[-1][-1]



if __name__ == "__main__":
    print(roll_dice(2,7))
    print(roll_dice(3,9))
    print(roll_dice(8,24))
