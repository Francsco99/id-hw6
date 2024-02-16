import Levenshtein
import re

str1='k-fast holding ab'
str2="k-fast holding ab (publ)"
str3='apple inc.'
str4='apple'


def norm_lev_dist(str1,str2):
    def normalize_text(stringa):
        return re.sub(r'[^a-zA-Z0-9]', '', stringa)
    dist = Levenshtein.distance(normalize_text(str1),normalize_text(str2))
    max_len = max(len(str1),len(str2))
    if max_len == 0:
        return 0
    return 1-(dist/max_len)

dist = Levenshtein.distance(str3,str4)
norm_dist = norm_lev_dist(str3,str4)

print(dist,norm_dist)

