class Button:
    def __init__(self, label: str, url: str):
        self.label = label
        self.url = url
    
    def to_dict(self):
        button_data = {"type": 2, "label": str(self.label), "style": 5, "url": str(self.url)}
        return button_data