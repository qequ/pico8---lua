import re


class Exporter:
    def __init__(self, filepath):
        self.filepath = filepath

    def export_to_lua(self):
        with open(self.filepath, mode='r') as f:
            cart_data = f.read()

        # the formatted data is a list with header, lua code and the
        # rest of gfx, map, sprites etc.
        formatted_data = re.split(r'__lua__|__gfx__', cart_data)
        code = formatted_data[1]

        path_lua_file = '/'.join((self.filepath).split('/')[:-1])
        lua_name = (self.filepath).split('/')[-1].split('.')[0] + '.lua'

        with open(path_lua_file + '/' + lua_name, mode='w') as new_file:
            new_file.write(code)
