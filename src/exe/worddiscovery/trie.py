_SENTINEL = object()

class _TrieNode(object):
    __slots__ = ('children', 'value', 'count')

    def __init__(self):
        self.children = {}
        self.value = _SENTINEL
        self.count = 0

    def __repr__(self):
        return '_TrieNode<%s>: value[%s], count[%d]' % (id(self), self.value, self.count)


class CharTrie(object):
    def __init__(self):
        self._root = _TrieNode()
        self.total_word_count = 0

    def insert(self, text):
        node = self._root
        for c in text:
            if c not in node.children:
                node.children[c] = _TrieNode()
                node.children[c].value = c
            node = node.children[c]
        node.count += 1
        self.total_word_count += 1

    def delete(self, text):
        pass

    def find(self, text):
        """
        Args:
            text: string
        Returns:
            count: int, frequent of text
        """
        is_in = True
        node = self._root
        for c in text:
            if c not in node.children:
                is_in = False
                break
            node = node.children[c]
        if is_in:
            return node.count
        else:
            return -1

    def traverse(self):
        Q = [(self._root, '')]

        while Q:
            node, prefix = Q.pop(0)
            for child in node.children.values():
                yield (child, prefix)
                Q.append((child, prefix+child.value))

    def get_all_words(self):
        for node, prefix in self.traverse():
            yield (prefix+node.value, node.count)

    def get_children_char_count(self, text):
        """
        function for entropy based word discovery
        """
        is_in = True
        node = self._root
        for c in text:
            if c not in node.children:
                is_in = False
                break
            node = node.children[c]

        children = []
        if is_in:
            for child in node.children.values():
                children.append((child.value, child.count))
        return children

    def clear(self):
        self._root = _TrieNode()
