from .auxiliary_methods import rect_intersect_generic, item_to_positions


class RotationType:
    RT_WHD = 0
    RT_HWD = 1
    RT_HDW = 2
    RT_DHW = 3
    RT_DWH = 4
    RT_WDH = 5

    ALL = [RT_WHD, RT_HWD, RT_HDW, RT_DHW, RT_DWH, RT_WDH]


class Axis:
    WIDTH = 0
    HEIGHT = 1
    DEPTH = 2

    ALL = [WIDTH, HEIGHT, DEPTH]


START_POSITION = [0, 0, 0]


class Item:
    def __init__(
        self, name, width, height, depth, weight, rotation_type=0, position=START_POSITION,
            valid_rotations=RotationType.ALL
    ):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.rotation_type = rotation_type
        self.volume = self.get_volume()
        self.valid_rotations = valid_rotations
        self.position = position

        assert self.rotation_type in self.valid_rotations
        assert not set(self.valid_rotations) - set(RotationType.ALL)

    def _reset(self):
        self.__init__(self.name, self.width, self.height, self.depth, self.weight)
        return

    def string(self):
        return "%s(%sx%sx%s, weight: %s) pos(%s) rt(%s)" % (
            self.name, self.width, self.height, self.depth, self.weight,
            self.position, self.rotation_type
        )

    def get_volume(self):
        return self.width * self.height * self.depth

    def get_dimension(self):
        if self.rotation_type == RotationType.RT_WHD:
            d = [self.width, self.height, self.depth]
        elif self.rotation_type == RotationType.RT_HWD:
            d = [self.height, self.width, self.depth]
        elif self.rotation_type == RotationType.RT_HDW:
            d = [self.height, self.depth, self.width]
        elif self.rotation_type == RotationType.RT_DHW:
            d = [self.depth, self.height, self.width]
        elif self.rotation_type == RotationType.RT_DWH:
            d = [self.depth, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WDH:
            d = [self.width, self.depth, self.height]
        else:
            d = []

        return d


class DummyItem(Item):
    def __init__(self):
        Item.__init__(self, 'Dummy_Item', 0, 0, 0, 0)


class Bin:
    def __init__(self, name, width, height, depth, max_weight):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.volume = self.get_volume()
        self.max_weight = max_weight
        self.items = []

    def string(self):
        return "%s(%sx%sx%s, max_weight:%s)" % (
            self.name, self.width, self.height, self.depth, self.max_weight
        )

    def get_volume(self):
        return self.width * self.height * self.depth

    def get_total_weight(self):
        total_weight = 0
        for item in self.items:
            total_weight += item.weight

        return total_weight

    def put_item(self, item):
        self.items.append(item)
        return

    """
    Checks if an item can be placed anywhere in a bin. Returns a tuple of the form:
        any_fit: Boolean. If there is at least a position and orientation where the item fits, True, else False
        details: List of tuples of the form [(Item, Position_1, Orientation_1)...(Item, Position_n, Orientation_n)] 
            where n is the total number of position-orientation pairs where there is fit. If param first_only==True,
            then only the first one will be returned
            
    """
    def check_fit_by_item(self, item, first_only=True):
        details = []
        any_fit = False
        # if first_only is not True: raise NotImplementedError
        if not self.items:
            _binned_items = [DummyItem()]
        else:
            _binned_items = self.items
        for binned_item in _binned_items:
            for position in set(item_to_positions(binned_item)):
                item.position = position
                fit, fit_details = self.check_fit_by_item_position(item, position, first_only=first_only)
                if fit:
                    any_fit = True
                    details += fit_details
                    if first_only:
                        break
        return any_fit, details

    """
    Checks if an item can be placed in a specific position of a bin. Returns a tuple of the form:
        any_fit: Boolean. If there is at least a position and orientation where the item fits, True, else False
        details: List of tuples of the form [(Item, Position_1, Orientation_1)...(Item, Position_n, Orientation_n)] 
            where n is the total number of position-orientation pairs where there is fit. If param first_only==True,
            then only the first one will be returned

    """
    def check_fit_by_item_position(self, item, position, first_only=True):
        details = []
        any_fit = False
        # if first_only is not True: raise NotImplementedError
        for rotation_type in RotationType.ALL:
            fit = self.check_fit_by_item_position_orientation(item, position, rotation_type)
            if fit:
                any_fit = True
                details.append((item, position, rotation_type))
                if first_only:
                    break
        return any_fit, details

    """
    Checks if an item can be placed in a specific position-rotation of a bin. Returns a single boolean:
        fit: Boolean.
    """
    def check_fit_by_item_position_orientation(self, item, position, rotation_type):
        fit = False
        # Check if weight exceeds limit
        if self.get_total_weight() + item.weight > self.max_weight:
            return fit
        # else:
        # Check if item fits inside bin for the given position and orientation
        item.rotation_type = rotation_type
        d = item.get_dimension()
        if (
                self.width < position[0] + d[0] or
                self.height < position[1] + d[1] or
                self.depth < position[2] + d[2]
        ):
            return fit
        # Check if item intersects with other items in the bin
        for binned_item in self.items:
            if intersect(item, binned_item):
                return fit
        fit = True
        return fit


class Packer:
    def __init__(self):
        self.bins = []
        self.items = []
        self.unbinned_items = []
        self.binned_items = []
        self.unfit_items = []
        self.total_items = 0

    def add_bin(self, bin):
        return self.bins.append(bin)

    def add_item(self, item):
        self.items.append(item)
        self.unbinned_items.append(item)
        self.total_items = len(self.items) + 1
        return

    def put_item_in_bin(self, bin, item, position, rotation_type):
        item.position = position
        item.rotation_type = rotation_type
        bin.put_item(item)
        self.binned_items.append(item)
        self.unbinned_items.remove(item)
        return

    def put_item_in_unfit(self, item):
        self.unfit_items.append(item)
        self.unbinned_items.remove(item)
        return

    def algorithm_1(self):
        _full_bins = []
        while True:
            _n = len(self.unbinned_items)
            for _bin in sorted(self.bins, key=lambda x: x.volume, reverse=True):
                for item in sorted(self.unbinned_items, key=lambda x: x.volume, reverse=True):
                    fitted, details = _bin.check_fit_by_item(item)
                    if fitted:
                        self.put_item_in_bin(_bin, *details[0])
                if _n == len(self.unbinned_items):
                    _full_bins.append(_bin)
            if _n != len(self.unbinned_items):
                _n = len(self.unbinned_items)
            else:
                break
        self.unfit_items = self.unbinned_items
        return

    def algorithm_2(self):  # Best fit decreasing
        while len(self.unbinned_items) > 0:
            _n = len(self.unbinned_items)
            for item in sorted(self.unbinned_items, key=lambda x: x.volume, reverse=True):
                fitted = False
                for _bin in sorted(self.bins, key=lambda x: x.volume - sum([i.volume for i in x.items]), reverse=True):
                    fitted, details = _bin.check_fit_by_item(item)
                    if fitted:
                        self.put_item_in_bin(_bin, *details[0])
                        break
                if fitted:
                    break
                self.put_item_in_unfit(item)
        return

    def custom_algorithm(self, func):
        return func(self)


def rect_intersect(item1, item2, x, y):
    return rect_intersect_generic(item1.position, item1.get_dimension(),
                                  item2.position, item2.get_dimension(), x, y)


def intersect(item1, item2):
    return (
        rect_intersect(item1, item2, Axis.WIDTH, Axis.HEIGHT) and
        rect_intersect(item1, item2, Axis.HEIGHT, Axis.DEPTH) and
        rect_intersect(item1, item2, Axis.WIDTH, Axis.DEPTH)
    )
