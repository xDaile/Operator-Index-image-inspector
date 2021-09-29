class ImageManager:
    s = 0

    def setup_image(self, image_address):
        print(image_address)
        self.local_image_address = image_address
        return self.local_image_address

    def get_local_address_of_image(self):
        return self.local_image_address