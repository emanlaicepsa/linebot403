def LCS(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if text1[i] == text2[j]:
                dp[i][j] = 1 if (i == 0 or j == 0) else (dp[i-1][j-1] + 1)
            if i > 0 and dp[i-1][j] > dp[i][j]:
                dp[i][j] = dp[i-1][j]
            if j > 0 and dp[i][j-1] > dp[i][j]:
                dp[i][j] = dp[i][j-1]
    return dp[m-1][n-1]

a = input()
b = input()
print(LCS(a,b))