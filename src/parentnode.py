from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag is present")
        if self.children is None:
            raise ValueError("No children are present")
        
        parent_start_string = f"<{self.tag}{self.props_to_html()}>"
        parent_end_string = f"</{self.tag}>"
        html_string = ""
        
        for node in self.children:
            html_string = html_string + node.to_html()
        return parent_start_string + html_string + parent_end_string
        
        
           
        