from tkinter import *
from tkinter import filedialog as fd

import os
from pixelate import pixelate

from PIL import Image, ImageTk

BASE_IMAGE_SIZE = 300


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.source_image = None
        self.result_image = None

        self.source_label = None
        self.result_label = None
        self.slider_label = None
        self.chunk_size = 25
        self.mode = IntVar()
        self.mode.set(1)

        self.create_widgets()

    @staticmethod
    def resized_image(image):
        ratio = max(map(lambda x: x/BASE_IMAGE_SIZE, image.size))
        return image.resize(tuple(map(lambda x: int(x/ratio), image.size)))

    @staticmethod
    def get_coords_for_resized_image(x, y, image):
        width, height = image.size

        if width > height:
            y += (BASE_IMAGE_SIZE - height) / 2
        else:
            x += (BASE_IMAGE_SIZE - width) / 2

        return {"x": x, "y": y}

    def update_slider(self, slider_value):
        self.slider_label['text'] = slider_value
        self.chunk_size = int(slider_value)
        self.create_result_image()

    def load_image(self):
        image_path = fd.askopenfilename(parent=self,
                                        filetypes=[('Image files', ('.png', '.jpg'))],
                                        title='Виберіть картинку',
                                        initialdir=os.path.join(os.getcwd(), 'examples'))

        if image_path:
            self.source_image = Image.open(image_path)
            resized_source_image = self.resized_image(self.source_image)

            source_photo = ImageTk.PhotoImage(resized_source_image)

            if self.source_label:
                self.source_label.configure(image=source_photo)
            else:
                self.source_label = Label(self.master, image=source_photo)

            self.source_label.image = source_photo
            self.source_label.place(**self.get_coords_for_resized_image(75, 50, resized_source_image))
            self.create_result_image()

    def save_image(self):
        if self.result_image:
            path = fd.asksaveasfilename(parent=self,
                                        filetypes=[('Image files', ('.png', '.jpg'))],
                                        title='Збережіть піксель-арт',
                                        initialdir=os.getcwd())
            if path:
                if path.split('.')[-1] not in ['jpg', 'png']:
                    self.result_image.save(path+'.png', 'PNG')
                else:
                    self.result_image.save(path, 'PNG')

    def create_result_image(self):
        if self.source_image:
            self.result_image = pixelate(self.source_image, self.chunk_size, self.mode.get())

            resized_result_image = self.resized_image(self.result_image)

            result_photo = ImageTk.PhotoImage(resized_result_image)

            if self.result_label:
                self.result_label.configure(image=result_photo)
            else:
                self.result_label = Label(self.master, image=result_photo)

            self.result_label.image = result_photo
            self.result_label.place(**self.get_coords_for_resized_image(425, 50, resized_result_image))

    def create_image_outlines(self):
        canvas = Canvas(self.master, width=800, height=500)
        canvas.create_rectangle(73, 48, 379, 354)  # Source image outline
        canvas.create_rectangle(423, 48, 729, 354)  # Result image outline
        canvas.pack()

    def create_buttons(self):
        source_btn_frame = Frame(self.master, width=302, height=50)
        result_btn_frame = Frame(self.master, width=302, height=50)

        source_btn_frame.pack_propagate(0)
        result_btn_frame.pack_propagate(0)

        source_btn_frame.place(x=75, y=360)
        result_btn_frame.place(x=425, y=360)

        select_button = Button(source_btn_frame, text='Вибрати картинку', font='arial 14', relief=GROOVE,
                               command=self.load_image)
        select_button.pack(fill=BOTH, expand=1)

        result_button = Button(result_btn_frame, text='Зберегти картинку', font='arial 14', relief=GROOVE,
                               command=self.save_image)
        result_button.pack(fill=BOTH, expand=1)

    def create_slider(self):
        self.slider_label = Label(self.master, text='25', font='arial 24')
        slider = Scale(self.master, from_=5, to=25, orient=HORIZONTAL, width=25, length=650, showvalue=0,
                       command=self.update_slider)
        slider.set(25)

        slider.place(x=75, y=420)
        self.slider_label.place(x=390, y=455)

    def create_mode_buttons(self):
        buttons_frame = Frame(self.master, width=400)

        rbutton1 = Radiobutton(buttons_frame, text='Повільно', variable=self.mode, value=1, indicatoron=0,
                               command=self.create_result_image)
        rbutton2 = Radiobutton(buttons_frame, text='Швидко', variable=self.mode, value=2, indicatoron=0,
                               command=self.create_result_image)

        rbutton1.pack(side=LEFT)
        rbutton2.pack(side=RIGHT)

        buttons_frame.place(x=340, y=20)

    def create_widgets(self):
        self.create_image_outlines()
        self.create_buttons()
        self.create_slider()
        self.create_mode_buttons()


if __name__ == '__main__':
    root = Tk()
    root.title('Pixel Art Maker')
    root.geometry('800x500')
    root.resizable(False, False)

    app = Application(master=root)
    app.mainloop()
