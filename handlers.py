import re
from pathlib import Path


def map_jumplines(s):
    if s.startswith('\n'):
        s = s[1:]

    if not s.endswith('\n'):
        s += '\n'

    return s


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

        return ("ok", lua_path)


class Importer(FileHandler):
    def __init__(self, filepath, lua_filepath):
        super(Importer, self).__init__(filepath)
        self.lua_filepath = lua_filepath

    def import_to_pico(self):
        # the code limit is 32k
        CARTRIDGE_CODE_LIMIT = 32768

        lua_size = Path(self.lua_filepath).stat().st_size

        if lua_size > CARTRIDGE_CODE_LIMIT:
            return 'fail_codesize'

        with open(self.filepath, mode='r') as cart_file:
            cart_data = cart_file.read()

        with open(self.lua_filepath, mode='r') as lua_file:
            lua_code = lua_file.read()

        cart_separators = ['__gfx__', '__gff__',
                           '__label__', '__map__', '__sfx__', '__music__']
        split_pattern = '__lua__'

        for cs in cart_separators:
            if cs in cart_data:
                split_pattern += '|' + cs

        formatted_data = re.split(split_pattern, cart_data)
        formatted_data[1] = lua_code

        sep_in_cart = split_pattern.split('|')
        index_to_insert = 1
        while len(sep_in_cart) != 0:
            sep_to_insert = sep_in_cart.pop(0)
            formatted_data.insert(index_to_insert, sep_to_insert)
            index_to_insert += 2

        formatted_data = map(map_jumplines, formatted_data)

        ready_to_write_data = ''.join(formatted_data)

        with open(self.filepath + '7', mode='w') as f:
            f.write(ready_to_write_data)

        return 'ok'
