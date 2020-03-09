from py3dbp import Packer, Bin, Item

packer = Packer()

packer.add_bin(Bin('small-envelope', 11.5, 6.125, 0.25, 0.8125))
packer.add_bin(Bin('large-envelope', 15.0, 12.0, 0.75, 0.8125))
packer.add_bin(Bin('small-box', 8.625, 5.375, 1.625, 70.0))
packer.add_bin(Bin('medium-box', 11.0, 8.5, 5.5, 70.0))
packer.add_bin(Bin('medium-box', 13.625, 11.875, 3.375, 70.0))
packer.add_bin(Bin('large-box', 12.0, 12.0, 5.5, 70.0))
packer.add_bin(Bin('large-box', 23.6875, 11.75, 3.0, 70.0))

packer.add_item(Item('50g [powder]', 3.9370, 1.9685, 1.9685, 50))
packer.add_item(Item('50g [powder]', 3.9370, 1.9685, 1.9685, 50))
packer.add_item(Item('50g [powder]', 3.9370, 1.9685, 1.9685, 50))
packer.add_item(Item('250g [powder]', 7.8740, 3.9370, 1.9685, 250))
packer.add_item(Item('250g [powder]', 7.8740, 3.9370, 1.9685, 250))
packer.add_item(Item('250g [powder]', 7.8740, 3.9370, 1.9685, 250))
packer.add_item(Item('250g [powder]', 7.8740, 3.9370, 1.9685, 250))
packer.add_item(Item('250g [powder]', 7.8740, 3.9370, 1.9685, 250))
packer.add_item(Item('250g [powder]', 7.8740, 3.9370, 1.9685, 250))


packer.algorithm_1()

for b in packer.bins:
    print(b.string())
    for i in b.items:
        print("====> ", i.string())
if packer.unfit_items:
    print('Unfit items')
    for b in packer.unfit_items:
        print("====> ", b.string())


