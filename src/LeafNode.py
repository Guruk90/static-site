from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("no Value")

        if self.tag is None or len(self.tag) == 0:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        html_str = f"<{self.tag}{self.props_to_html()}"
        html_str += ">"
        return f"{html_str}{self.value}</{self.tag}>"
