from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None or len(self.tag) == 0:
            raise ValueError("missing Tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("missing Children")

        if self.props is not None:
            html_string = f"<{self.tag}{self.props_to_html()}>"
        else:
            html_string = f"<{self.tag}>"

        for node in self.children:
            html_string += node.to_html()
        html_string += f"</{self.tag}>"

        return html_string
