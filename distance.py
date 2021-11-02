# This file provides functions that can deal with typos of user input according to the similarity/distance between words

def levenshtein_distance(str1, str2):
    if len(str2) == 0:
        return len(str1)
    elif len(str1) == 0:
        return len(str2)
    elif str1[0] == str2[0]:
        return levenshtein_distance(str1[1:], str2[1:])
    else:
        a = 1 + levenshtein_distance(str1, str2[1:])
        b = 1 + levenshtein_distance(str1[1:], str2[1:])
        c = 1 + levenshtein_distance(str1[1:], str2)
        return min(a, b, c)

def damerau_levenshtein(a, b, i, j):
    '''
    Initailly, 
        i = len(a) - 1
        j = len(b) - 1
    '''
    if i < 0:
        return max(j + 1, 0)
    elif j < 0:
        return max(i + 1, 0)
    elif a[i] == b[j]:
        return damerau_levenshtein(a, b, i - 1, j - 1)
    elif i > 0 and j > 0 and a[i] == b[j - 1] and a[i - 1] == b[j]:
        v1 = 1 + damerau_levenshtein(a, b, i - 1, j) # deletion
        v2 = 1 + damerau_levenshtein(a, b, i, j - 1) # deletion
        v3 = 1 + damerau_levenshtein(a, b, i - 1, j - 1) # substitution
        v4 = 1 + damerau_levenshtein(a, b, i - 2, j - 2) # transposition
        return min(v1, v2, v3 ,v4)
    elif i >= 0 and j >= 0:
        v1 = 1 + damerau_levenshtein(a, b, i - 1, j) # deletion
        v2 = 1 + damerau_levenshtein(a, b, i, j - 1) # deletion
        v3 = 1 + damerau_levenshtein(a, b, i - 1, j - 1) # substitution
        return min(v1, v2, v3)
      
