class Term():
    def __init__(self, name):
        self.name = name
        self.count = 0

    def set_tf(self, words_count):
        tf = self.count / words_count
        self.tf = tf

    def count_up(self):
        self.count += 1
