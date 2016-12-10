
class Ranges:
    """ Stores a list of video frame ranges with different meanings.
        Internal storage format for example:
        [ ['ad', 0.345, 0.376],
          ['preview', 0.377, 0.423],
          ['ad', 0.5],  # Incomplete range (end to be set)
          ...
        ]
        where the float numbers are start and end in the [0, 1] interval of the whole movie.
        On change, it calls the update_function
    """
    def __init__(self, update_function):
        self.ranges = []
        self.update_function = update_function

    def last_is_incomplete(self):
        if len(self.ranges) > 0:
            if len(self.ranges[-1]) < 3:
                return True
        return False

    def add_range_start(self, type, start):
        if self.last_is_incomplete():
            self.remove_last_element()

        # Append new incomplete range
        self.ranges.append([type, start])

        self.update_function(self.ranges)

    def add_range_end(self, end):
        if self.last_is_incomplete():
            self.ranges[-1].append(end)

        self.update_function(self.ranges)

    def remove_last_element(self):
        """Remove end of last range, or if incomplete remove range.
        Works very much like an UNDO function"""
        if len(self.ranges) > 0:
            if self.last_is_incomplete():
                # Remove last range
                del self.ranges[-1]
            else:
                # Remove last element of last range
                del self.ranges[-1][-1]

            self.update_function(self.ranges)

    def get_ranges(self):
        return self.ranges

    def set_ranges(self, range_data):
        assert(isinstance(range_data, list))
        self.ranges = range_data
        self.update_function(self.ranges)
