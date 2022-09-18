class Session:
    """ Represents a shell session """

    def __init__(self, id, uid, curr_dir):
        self.id = id
        self.uid = uid
        self.curr_dir = curr_dir

    def get_curr_dir(self):
        return self.curr_dir

    def get_uid(self):
        return self.uid

    def get_id(self):
        return self.id