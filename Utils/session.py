from datetime import datetime

class Session:
    def __init__(self, uuid):
        self.uuid = uuid
        self.timestamp = datetime.now()
        self.images = []
        self.links = []
        self.loading_count = 0 # number of conversions
    def add_image(self, image_path):
        self.images.append(image_path)
    def add_link(self, link):
        self.links.append(link)

