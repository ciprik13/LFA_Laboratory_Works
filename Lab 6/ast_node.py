class ASTNode:
    def __init__(self, kind, value=None, children=None):
        self.kind = kind
        self.value = value
        self.children = children or []

    def add_child(self, node):
        self.children.append(node)

    def __str__(self, level=0):
        ret = "\t" * level + f"{self.kind}: {self.value if self.value else ''}\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret
