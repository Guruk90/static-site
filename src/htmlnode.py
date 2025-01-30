class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_str = ""
        for key in self.props:
            html_str += " " + key + '="' + self.props[key]+'"'
        return html_str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        # First, check if other is also an HTMLNode
        if not isinstance(other, HTMLNode):
            return False

        if self.tag != other.tag:
            return False

        if self.value != other.value:
            return False

        if self.props != other.props:
            return False

            # Are both None?
        if self.children is None and other.children is None:
            return True
            # Is one None and the other isn't?
        if self.children is None or other.children is None:
            return False
            # Do they have different numbers of children?
        if len(self.children) != len(other.children):
            return False
            # Compare all children (Python will use __eq__ recursively)
        return all(a == b for a, b in zip(self.children, other.children))
