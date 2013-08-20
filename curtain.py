import array, socket
from random import randint

width = 15
height = 5
# frame_length = 0.6 #0.005
# frame_length = 0.03
frames_per_second = 30
frame_length = 1.0 / frames_per_second

brightness = 0.3 #0.012 dim  # 0.08 bright

id_grid = [[292, 418, 328, 256, 625],
           [529, 601, 592, 493, 319],
           [445, 388, 697, 655, 682],
           [709, 337, 718, 472, 346],
           [None, 301, 745, 277, None]]
id_map = {}
for x in range(width):
    for y in range(height):
        grid_value = id_grid[y][x / 3]
        if grid_value != None:
            id_map[x, y] = grid_value - 256 + (x % 3) * 3

def array_to_bytes(byte_array):
    return array.array('B', byte_array).tostring()

packet_header_array = [0x04, 0x01, 0xdc, 0x4a, 0x01, 0x00, 0x01, 0x01,
                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                       0xff, 0xff, 0xff, 0xff, 0x00]
packet_header = array_to_bytes(packet_header_array)

class Curtain(object):
    def __init__(self, host='10.0.63.101', port=6038):
        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1)

    def send_packet(self, packet):
        self.socket.sendto(packet, (self.host, self.port))

    def send_color_dict(self, color_dict):
        array = [0x00] * 512

        for x in range(width):
            for y in range(height):
                if (x, y) in id_map and (x, y) in color_dict:
                    colors = [int(min(max(0, color), 1) * 255) for color in color_dict[x, y]]

                    index = id_map[x, y]
                    array[index:index+3] = colors

        self.send_packet(packet_header + array_to_bytes(array))

class Canvas(dict):
    width = 15
    height = 5

    def __init__(self):
        self.clear()

    def draw_pixel(self, x, y, r, g, b):
        self[x, y] = r, g, b

    def add_pixel(self, x, y, r, g, b):
        r1, g1, b1 = self[x, y]
        self[x, y] = r1 + r, g1 + g, b1 + b

    def draw_letter(self, letter, offset_x, offset_y, r, g, b):
        for x, y in letter.pixel_list:
            self.draw_pixel(offset_x + x, offset_y + y, r, g, b)

    def add_letter(self, letter, offset_x, offset_y, r, g, b):
        for x, y in letter.pixel_list:
            self.add_pixel(offset_x + x, offset_y + y, r, g, b)

    def clear(self, r=0, g=0, b=0):
        for x in range(self.width):
            for y in range(self.height):
                self[x, y] = (r, g, b)

