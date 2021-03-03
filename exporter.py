import re


class FileHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def get_parent_dir(self):
        return '/'.join((self.filepath).split('/')[:-1])

    def create_lua_filepath(self):
        par_dir = self.get_parent_dir()
        lua_name = (self.filepath).split('/')[-1].split('.')[0] + '.lua'
        return par_dir + '/' + lua_name


class Exporter(FileHandler):
    def __init__(self, filepath):
        super(Exporter, self).__init__(filepath)

    def export_to_lua(self):
        with open(self.filepath, mode='r') as f:
            cart_data = f.read()

        # the formatted data is a list with header, lua code and the
        # rest of gfx, map, sprites etc.
        formatted_data = re.split(r'__lua__|__gfx__', cart_data)
        code = formatted_data[1]

        lua_path = self.create_lua_filepath()

        with open(lua_path, mode='w') as new_file:
            new_file.write(code)
