# colors are 0-255
import array, time, socket

def array_to_bytes(byte_array):
    return array.array('B', byte_array).tostring()

packet_header_array = [0x04, 0x01, 0xdc, 0x4a, 0x01, 0x00, 0x01, 0x01,
                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                       0xff, 0xff, 0xff, 0xff, 0x00]

packet_header = array_to_bytes(packet_header_array)



class CK(object):
    def __init__(self, host='10.0.9.54', port=6038):
        self.ck_colors = [(255,255,255),(255,255,255),(255,255,255)]
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1)
    


    def set_color(self, ckID, color):
        self.ck_colors[ckID] = color

    def update(self):
        array = [0x00] * 512

        for i in range(len(self.ck_colors)):
            for j in range(3):
                array[(i * 3) + j] = self.ck_colors[i][j]
        
        packet = packet_header + array_to_bytes(array)

        self.socket.sendto(packet, (self.host, self.port))


if __name__ == "__main__":
    yeadude = CK()

    while(1):
        yeadude.update()
        time.sleep(.35)


