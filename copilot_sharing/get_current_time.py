# Manacher's Algorithm for finding the longest palindromic substring
# return subtring

def longest_palindromic_substring(s):
    # preprocess
    s = '#' + '#'.join(s) + '#'
    n = len(s)
    p = [0] * n
    c = 0
    r = 0
    for i in range(1, n - 1):
        p[i] = min(r - i, p[2 * c - i]) if r > i else 0
        while i - 1 - p[i] >= 0 and i + 1 + p[i] < n and s[i - 1 - p[i]] == s[i + 1 + p[i]]:
            p[i] += 1
        if i + p[i] > r:
            c = i
            r = i + p[i]
    maxLen = 0
    centerIndex = 0
    for i in range(1, n - 1):
        if p[i] > maxLen:
            maxLen = p[i]
            centerIndex = i
    return s[centerIndex - maxLen: centerIndex + maxLen + 1].replace('#', '')

# unit test
if __name__ == '__main__':
    s = 'abacdfgdcaba'
    assert longest_palindromic_substring(s) == 'aba'
    s = 'abacdfdcaba'
    assert longest_palindromic_substring(s) == 'abacdfdcaba'
    s = ''
    assert longest_palindromic_substring(s) == ''
    s = 'a'
    assert longest_palindromic_substring(s) == 'a'