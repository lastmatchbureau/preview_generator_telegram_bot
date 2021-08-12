from PIL import Image
import os


class PreviewGenerator:
    X_MARGIN = 30
    Y_MARGIN = 30

    def __init__(self, img_names=None, base_img_width=None, base_img_height=None):
        self.found = False
        self.img_names = img_names
        self.base_img_width = base_img_width
        self.base_img_height = base_img_height
        self.images = []
        self.mode = "CMYK"

    def get_size(self, length: int) -> tuple[int, int]:
        return int((self.base_img_width + self.X_MARGIN) * length + self.X_MARGIN), \
               int(self.base_img_height + self.Y_MARGIN * 2)

    def find_images(self, folder_path: str):
        self.img_names = []
        for root, dir, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if ".png" in file or "preview" in file:
                    self.img_names.append(file_path)
                    self.found = True

    def get_images(self):
        for name in self.img_names:
            img = Image.open(name)
            self.images.append(img)
            print(name, img.mode)
            self.mode = img.mode
            if self.base_img_width is None:
                self.base_img_width = img.width
                self.base_img_height = img.height

    def clear_all(self):
        self.found = False
        self.img_names = None
        self.base_img_width = None
        self.base_img_height = None
        self.images = []

    def run(self, folder_path: str):
        print("START")
        self.find_images(folder_path)
        if self.found:
            self.get_images()

            preview_size = self.get_size(len(self.images))

            if self.mode == "RGB":
                self.mode = "RGBA"
            preview = Image.new(self.mode, size=preview_size)

            x = self.X_MARGIN
            y = self.Y_MARGIN
            for img in self.images:
                preview.paste(img, (x, y))
                x = x + img.width + self.X_MARGIN

            preview.save(os.path.join(folder_path, "preview.png"))
            self.clear_all()
        print("DONE")


if __name__ == "__main__":
    try:
        gen = PreviewGenerator()
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()

        folder_path = filedialog.askdirectory()
        folder_path = folder_path.replace("/", "\\")
        counter = 0
        for root, dir, files in os.walk(folder_path):
            for directory in dir:
                print(f"completed: {counter} of {len(dir)}")
                directory_path = os.path.join(root, directory)
                print(f"---- {directory_path} ----")
                gen.run(directory_path)
                print(f"---- {directory_path} completed ----")
                counter += 1
            break
    except Exception as e:
        print(e.args)
    input()