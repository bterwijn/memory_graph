
def find_kmer_positions(dna, k):
    positions = {}
    for i in range(len(dna) - k + 1):
        kmer = dna[i:i+k]
        if kmer not in positions:
            positions[kmer] = []
        positions[kmer].append(i)
    return positions


dna = "ACGTTGCATGTCGCATGATGCATGAGAGCT"
k = 4

result = find_kmer_positions(dna, k)
for kmer, positions in result.items():
    print(f'{kmer}: {positions}')
