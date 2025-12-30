import random

mg.config.type_to_horizontal[list] = True

END = "_end_"

def build_trie(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node[END] = True
    return root

def word_completions(trie, prefix):
    results = []

    def depth_first_search(node, prefix):
        if END in node:
            results.append(prefix)
        for ch, child in node.items():
            if ch != END:
                depth_first_search(child, prefix + ch)

    node = trie
    for ch in prefix:
        if ch in node:
            node = node[ch]
        else:
            return []
    depth_first_search(node, prefix)
    return results
    
words = ["to", 
         "too", "top", "toy", "ton", "toe", "tor", 
         "torn", "tore", "toss", "told", "toll", "tone"]
random.shuffle(words)
trie = build_trie(words)

print( word_completions(trie, "to") )
print( word_completions(trie, "tor") )
