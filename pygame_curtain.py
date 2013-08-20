from curtain import width, height

class PygameCurtain(object):
    def init(self):
        self.width = width
        self.height = height

    def send_color_dict(self, color_dict):
        """
        Render the `color_dict`.

        `color_dict` is a dict where the keys are tuples
        in the bounds of `width` and `height` and the values
        are tuples of r, g, b.
        """
        raise NotImplementedError()
