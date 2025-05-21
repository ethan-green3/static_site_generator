class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        if children is None:
            self.children = []
        else:    
            self.children = children
        if props is None:
            self.props = dict()
        else:
            self.props = props

    def to_html(self):
        pass
            
    
    def props_to_html(self):
        if not self.props:
            return ""
        html_string = ""
        for key, value in self.props.items():
            html_string = html_string + f' {key}="{value}"'
        return html_string
    
    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"