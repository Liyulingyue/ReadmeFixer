def longest_common_subsequence(str1, str2):
    m, n = len(str1), len(str2)
    # 创建一个二维数组来存储子问题的解
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 填充dp数组
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 返回最长公共子序列的长度
    return dp[m][n]


def lcs_similarity_index(str1, str2):
    # 计算最长公共子序列的长度
    lcs_len = longest_common_subsequence(str1, str2)
    # 计算两个字符串中的最大长度
    max_len = max(len(str1), len(str2))
    # 计算相似性指标（最长公共子序列长度 / 最大字符串长度）
    similarity_index = lcs_len / max_len
    difference_number = max_len - lcs_len
    return similarity_index, difference_number


# 示例
# print(lcs_similarity_index("hellop", "hrp"))  # 输出一个小于1的值，具体取决于LCS的长度
# print(lcs_similarity_index("hello", "olleh"))  # 输出一个小于1的值，具体取决于LCS的长度