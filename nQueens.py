#-*-coding:utf-8-*-

'''
    N皇后问题，经典的回溯法例子
'''
n = 8
track = [-1] * n
count = 0


def nQueens(k):
    global track, n, count
    if k >= n:
        count += 1
        print(track)
    else:
        for i in range(n):
            track[k] = i
            if isPlaced(k):
                nQueens(k+1)


def isPlaced(i):
    j = 0
    global track
    while j < i:
        if track[i] == track[j] or abs(track[i] - track[j]) == abs(i-j):
            return False
        j += 1
    return True

if __name__ == '__main__':
    nQueens(0)
    print(count)
