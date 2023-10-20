import sys
import Repository
from DTO import *


def main(args):
    print(args)
    repo = Repository._Repository(args[4])
    repo.create_tables()
    repo._commit()
    file = open(args[1],'r')
    file.readline()
    for line in file:
        line = line.split("\n")[0]
        if len(line.split(",")) == 4:
            hat_id = line.split(',')[0]
            topping = line.split(',')[1]
            supplier_id = line.split(',')[2]
            quantity = line.split(',')[3]
            toInsert = Hat(hat_id, topping, supplier_id, quantity)
            repo.hats.insert(toInsert)
        else:
            supplier_id = line.split(',')[0]
            supplier_Name = line.split(',')[1]
            toInsert = Supplier(supplier_id, supplier_Name)
            repo.suppliers.insert(toInsert)
    file = open(args[2],'r')
    orderID = 1
    output = open(args[3], 'w')
    for line in file:
        line = line.split("\n")[0]
        location = line.split(',')[0]
        topping = line.split(',')[1]
        hatToOrder = repo.hats.find(topping)
        supplier = repo.suppliers.find(hatToOrder.supplier).name
        orderToInsert = Order(orderID, location, hatToOrder.id)
        repo.orders.insert(orderToInsert)
        orderID += 1
        output.write(topping + "," + supplier + "," + location + "\n")
        if hatToOrder.quantity > 0:
            repo.hats.updateQuantity(hatToOrder.id, hatToOrder.quantity-1)
        if hatToOrder.quantity-1 == 0:
            repo.hats.removeByQuantity(hatToOrder.id)
    output.close()
    sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)