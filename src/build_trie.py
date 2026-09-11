import memory_graph as mg
import random

# horizontal lists
mg.config.type_to_horizontal[list] = True

END = "_end_"

def build_trie(words):
    root = {}
    for w in words:
        qw = f'"{w}"'
        print(f'add {qw:7}:', end=' ')
        node = root
        for ch in w:
            print(ch, end=' ')
            node = node.setdefault(ch, {})
        node[END] = True
        print()
    return root

def word_completions(trie, prefix):
    results = []

    def depth_first_search(node, prefix):
        if END in node:
            results.append(prefix)
        for ch, child in node.items():
            if ch != END:
                depth_first_search(child, prefix + ch)

    print(f'\ncomplete "{prefix}..." :', end=' ')
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
print('build the Trie')
trie = build_trie(words)

print( word_completions(trie, "tor") )
print( word_completions(trie, "to") )
