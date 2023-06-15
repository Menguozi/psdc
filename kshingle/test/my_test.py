import kshingle as ks
shingles = ks.shingleset_k("aBc DeF", k=5)  # -> 25 shingles
print(len(shingles))
shingles = shingles.union(
    ks.wildcard_shinglesets(shingles, n_max_wildcards=2))  # -> 152 shingles
print(len(shingles))