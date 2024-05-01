from sympy import proper_divisors
import matplotlib.pyplot as plt

class AliquotSequence:
    def __init__(self, **kwargs):
        if 'n' in kwargs:
            self.sequence = [kwargs['n']]
        elif 'sequence' in kwargs:
            self.sequence = kwargs['sequence']
        elif 'path_to_elf_file' in kwargs:
            self.sequence = []
            self.load_from_elf_file(kwargs['path_to_elf_file'])
        elif 'root_from_elf' in kwargs:
            path_to_elf_file = f"data/{kwargs['root_from_elf']}.elf"
            self.sequence = []
            self.load_from_elf_file(path_to_elf_file)
        else:
            raise ValueError("Invalid arguments")
        
        if 'completed' in kwargs:
            self.completed = kwargs['completed']
        else:
            self.completed = False

    def load_from_elf_file(self, path_to_elf_file):
        # load sequence from elf file, each line is: 0 .   276 = 2^2 * 3 * 23
        with open(path_to_elf_file, 'r') as f:
            for line in f:
                n = int(line.split()[2])
                self.sequence.append(n)
        print(f"Loaded sequence of length {len(self.sequence)} from {path_to_elf_file}")

    def compute_next(self):
        if self.completed: # already computed the whole sequence
            return
        n = self.sequence[-1] # last element

        factors = proper_divisors(n) # sympy
        next_n = sum(factors)

        # check completion
        if next_n == 1: # reached 1
            self.completed = True
            print(f"Sequence completed after {len(self.sequence)} steps by reaching 1")
        if next_n in self.sequence: # reached a cycle
            self.completed = True
            print(f"Sequence completed after {len(self.sequence)} steps by reaching a cycle")

        self.sequence.append(next_n) # add to sequence

    def compute_all(self, n=10_000): # stop after 10k iterations
        i = 0
        while not self.completed and i < n:
            self.compute_next()
            i += 1

    def magnitude(self):
        return len(self.sequence)

    def root(self):
        return self.sequence[0]

    def plot(self):
        plt.clf()
        plt.plot(self.sequence)

        plt.yscale('log')
        plt.grid()

        comp_str = "(complete)" if self.completed else "(incomplete)"
        plt.title(f"Aliquot sequence starting at {self.root()} with length {len(self.sequence)} {comp_str}")

        plt.xlabel("Step")
        plt.ylabel("Value")
        
        plt.savefig("plot.png")

lehmer_five = [AliquotSequence(root_from_elf=n) for n in [276, 552, 564, 660, 966]]

lehmer_sets = [set(sequence.sequence) for sequence in lehmer_five]
intersection = lehmer_sets[0].intersection(*lehmer_sets[1:])
print(f"Length of intersection of all sequences: {len(intersection)}") # 0 -> no common elements

lehmer_five[0].plot()

sequence_980460 = AliquotSequence(n=980460)
sequence_980460.compute_all()

sequence_980460.plot()