class Session:
    """ Represents a shell session """

    def __init__(self, id, uid, curr_dir):
        self.id = id
        self.uid = uid
        self.curr_dir = curr_dir