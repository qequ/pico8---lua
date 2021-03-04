import tkinter as tk
from tkinter import filedialog
from handlers import Exporter, Importer
import os


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

        self.lbl_status = tk.Label(master=self, text='Awaiting paths')
        self.lbl_filepath_pico = tk.Label(master=self, text='No file selected')
        self.lbl_filepath_lua = tk.Label(master=self, text='No file selected')
        self.btn_filepath_pico = tk.Button(
            master=self, text='Browse pico-8 file', command=self.browse_filepath_pico)
        self.btn_filepath_lua = tk.Button(
            master=self, text='Browse lua file', command=self.browse_filepath_lua)

        self.btn_main_page = tk.Button(
            master=self, text='Back to Main Menu', command=lambda: controller.show_frame('StartPage'))

        self.btn_import = tk.Button(
            master=self, text='Import the Lua code to Pico-8', command=self.import_code)

        self.lbl_status.grid(row=0, column=0)
        self.lbl_filepath_pico.grid(row=1, column=0)
        self.btn_filepath_pico.grid(row=1, column=1)
        self.lbl_filepath_lua.grid(row=2, column=0)
        self.btn_filepath_lua.grid(row=2, column=1)
        self.btn_main_page.grid(row=3, column=1)
        self.btn_import.grid(row=3, column=0)

    def browse_filepath_pico(self):
        filename = filedialog.askopenfilename(
            initialdir='~/.lexaloffle/pico-8/carts', title='select cart', filetypes=(("PICO-8 files (.p8)", "*.p8"),))
        self.lbl_filepath_pico.configure(text=filename)
        self.lbl_status.configure(text='.P8 file loaded succesfully!')

    def browse_filepath_lua(self):
        filename = filedialog.askopenfilename(
            initialdir='~/', title='select lua file', filetypes=(("Lua files (.lua)", "*.lua"),))
        self.lbl_filepath_lua.configure(text=filename)
        self.lbl_status.configure(text='Lua file loaded succesfully!')

    def import_code(self):
        if not os.path.exists(self.lbl_filepath_lua['text']) or not os.path.exists(self.lbl_filepath_pico['text']):
            self.lbl_status.configure(text='Unable to Import - Missing files')
            return

        imp = Importer(
            self.lbl_filepath_pico['text'], self.lbl_filepath_lua['text'])

        ans = imp.import_to_pico()
        if ans == 'ok':
            self.lbl_status.configure(text='Imported Succesfully to the Cart!')
        elif ans == 'fail_codesize':
            self.lbl_status.configure(
                text='Unable to Import - Lua code size is bigger than allowed.')
        else:
            self.lbl_status.configure(text='Unable to Import')


class Export(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.btn_browse_file = tk.Button(
            master=self, text='Browse File', command=self.browse_filepath)
        self.lbl_filename = tk.Label(master=self, text='No file selected')

        self.lbl_filename.grid(row=0, column=0)
        self.btn_browse_file.grid(row=0, column=1)

        self.btn_main_page = tk.Button(
            master=self, text='Back to Main Menu', command=lambda: controller.show_frame('StartPage'))
        self.btn_main_page.grid(row=1, column=1)

        self.btn_export = tk.Button(
            master=self, text='Export the cart to Lua', command=self.export_cartridge)
        self.btn_export.grid(row=1, column=0)

    def browse_filepath(self):
        filename = filedialog.askopenfilename(
            initialdir='~/.lexaloffle/pico-8/carts', title='select cart', filetypes=(("PICO-8 files (.p8)", "*.p8"),))
        self.lbl_filename.configure(text=filename)

    def export_cartridge(self):
        if ' ' in self.lbl_filename['text']:
            return
        exp = Exporter(self.lbl_filename['text'])
        ans, lua_path = exp.export_to_lua()

        if ans == 'ok':
            status = 'Exported sucessfully!\n lua file path: {}'.format(
                lua_path)
        else:
            status = 'Unable to export the lua code.'

        self.lbl_filename.configure(text=status)


if __name__ == '__main__':
    app = App()
    app.mainloop()
