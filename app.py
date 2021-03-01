import tkinter as tk


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('pico8 <-> Lua')
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for FrameClass in [StartPage, Import, Export]:
            page_name = FrameClass.__name__
            print(page_name)
            frame = FrameClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        btn_export = tk.Button(
            master=self, text='Pico -> Lua', command=lambda: controller.show_frame('Export'))
        btn_import = tk.Button(
            master=self, text='Lua -> Pico', command=lambda: controller.show_frame('Import'))

        btn_export.grid(row=0, column=0, padx=10)
        btn_import.grid(row=1, column=0, pady=10)


class Import(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        btn_main_page = tk.Button(
            master=self, text='Back to Main Menu', command=lambda: controller.show_frame('StartPage'))
        btn_main_page.pack()


class Export(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        btn_main_page = tk.Button(
            master=self, text='Back to Main Menu', command=lambda: controller.show_frame('StartPage'))
        btn_main_page.pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()
