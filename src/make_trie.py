
def make_trie(words):
    root = {}
    END = "_end_"
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node[END] = True
    return root

words = ["to", 
         "too", "top", "toy", "ton", "toe", 
         "torn", "tore", "toss", "told", "toll", "tone"]
trie = make_trie(words)
