from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        html_str = f"<{self.tag}"
        for key in self.props:
            html_str += " " + key + '="' + self.props[key]+'"'
        html_str += ">"
        return f"{html_str}{self.value}</{self.tag}>"
