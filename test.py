from py3dbp import Item, Bin, Packer
print('start')
from copy import deepcopy

packer = Packer()

packer.add_bin(Bin('small-envelope 1', 85, 85, 85, 124))

for j in range(11):
    a = Item('Beauty & Personal Care {}'.format(j), 19, 19, 19, 12)
    packer.add_item(a)

for j in range(14):
    a = Item('Tools & Home Improvement {}'.format(j), 6, 6, 6, 4)
    packer.add_item(a)
    
for j in range(8):
    a = Item('Audible Books & Originals {}'.format(j), 15, 15, 15, 8)
    packer.add_item(a)

import time
now = time.time()
packer_1 = deepcopy(packer)
packer_2 = deepcopy(packer)

packer = packer_1
packer.algorithm_1()
print('start')
for b in packer.bins:
    print(b.string())
    for i in b.items:
        print("====> ", i.string())
if packer.unfit_items:
    print('Unfit items')
    for b in packer.unfit_items:
        print("====> ", b.string())

packer = packer_2
packer.algorithm_2()

print('start')
for b in packer.bins:
    print(b.string())
    for i in b.items:
        print("====> ", i.string())
if packer.unfit_items:
    print('Unfit items')
    for b in packer.unfit_items:
        print("====> ", b.string())
print(time.time() - now)