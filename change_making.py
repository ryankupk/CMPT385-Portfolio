
def change_making(d,n):
    # Your code goes here:
    #initialize array of zeroes 1 longer than n
    F = [0]*(n+1)
    #first index is always 0, second index is always 1
    F[1] = 1
    for i in range(2,n + 1): #i represents value of coin in question
        temp = []
        for j in range(len(d)):
            #for each denomination, if it's less than i, it can be subtracted from i
            if i >= d[j]:
                #index F array at i - d[j] (number of coins needed to make i-d[j]), then add 1 because it will take one additional coin to make i
                temp.append(F[i-d[j]] + 1)
        #F[i] is the smallest value of temp array
        F[i] = min(temp)
    return F[-1]





if __name__ == "__main__":
    d=[1,3,4,5,6]
    n=10
    print(change_making(d,n))
    
    d=[1,2,4,6,8,10,22,23]
    n=40
    print(change_making(d,n))

    d=[1,2,10,11,12,15,19,30]
    n=1900
    print(change_making(d,n))

