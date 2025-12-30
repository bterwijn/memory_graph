import random

END = "_end_"

def make_trie(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node[END] = True
    return root

def complete_words(trie, start):
    results = []

    def dfs(node, prefix):
        if END in node:
            results.append(prefix)
        for ch, child in node.items():
            if ch != END:
                dfs(child, prefix + ch)

    node = trie
    for ch in start:
        if ch in node:
            node = node[ch]
        else:
            return []
    dfs(node, start)
    return results
    
words = ["to", 
         "too", "top", "toy", "ton", "toe", "tor", 
         "torn", "tore", "toss", "told", "toll", "tone"]
random.shuffle(words)
trie = make_trie(words)

print( complete_words(trie, "to") )
print( complete_words(trie, "tor") )
