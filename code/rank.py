import os.path
import pickle
class Rank:
    def __init__(self):
        self.file = "rank.dat"

        if os.path.isfile(self.file):
            f = open('rank.dat', 'rb')
            flist = pickle.load(f)
            f.close()
        else:
            flist = []

        self.ranklist = flist

    def save(self):
        f = open('rank.dat', 'wb')
        pickle.dump(self.ranklist, f)
        f.close()

    def setrec(self, score):
        if len(self.ranklist) > 10:
            for r in self.ranklist:
                if score > r:
                    self.ranklist.append(score)
                    break
        else:
            self.ranklist.append(score)

        self.ranklist.sort(reverse = True)
        
        while len(self.ranklist) > 10:
            self.ranklist.pop()
