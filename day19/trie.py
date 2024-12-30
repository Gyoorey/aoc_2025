

class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for letter in word:
            if letter not in node:
                node[letter] = {}
            node = node[letter]
        node["#"] = "#" # to indicate the end of the word
    
    def startsWithAll(self, prefix):
        node = self.root
        indices = []
        for i, letter in enumerate(prefix):
            if letter not in node:
                break
            node = node[letter]
            if "#" in node:
                indices.append(i+1)
        return indices