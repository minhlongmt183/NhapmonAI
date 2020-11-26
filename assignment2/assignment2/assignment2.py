# Them cac thu vien neu can
from functools import reduce

def read_input(file_input):
    with open(file_input, "r") as f:
        # get depot_coordinates
        depot_coord         = {}
        data                = f.readline().split(' ') 
        depot_coord["x"]    = int(data[0])
        depot_coord["y"]    = int(data[1])

        # get number employees and number packages
        data                = f.readline().split(' ')
        number_packages     = int(data[0])
        number_employees    = int(data[1])

        # get infor of packages
        packages = []
        employees = [None]*number_employees

        for i in range(number_packages):
            package         = {}
            package_info    = f.readline().split(' ')

            package["id"]           = int(i)
            package["dest_coord_x"] = int(package_info[0])
            package["dest_coord_y"] = int(package_info[1])
            package["volume"]       = int(package_info[2])
            package["weight"]       = int(package_info[3])

            packages.append(package)
        
    return depot_coord, packages, employees

def write_output(employees,file_output):
    with open(file_output, "w") as f:
        for employee in employees:
            for package in employee:
                f.write("{} ".format(package))
            f.write("\n")

def algorithm(depot_coord, packages, employees):
    # A_start
    inital_state

    return employees

def profit(employee, packages, depot_coord):
    
    energy      =   [(5 + packages[i]["volume"] + (packages[i]["weight"] * 2)) for i in employee]

    distances   =   ((packages[0]["dest_coord_x"] - depot_coord["x"])** 2 \
                +    (packages[0]["dest_coord_y"] - depot_coord["y"])** 2)**.5
    
    for i in range(1, len(packages)):
        distances   +=  ((packages[i]["dest_coord_x"] - packages[i-1]["dest_coord_x"])** 2 \
                    +   (packages[i]["dest_coord_y"] - packages[i-1]["dest_coord_y"])** 2)**.5

    revenue     = reduce(lambda x,y: x+y, energy, 0)
    expenses    = distances / 40 * 20 + 10
    profit      = revenue - expenses
    return profit

def assign(file_input, file_output):
    # read input
    depot_coord, packages, employees = read_input(file_input)

    # print(packages)

    print(profit([0,3], packages, depot_coord))

    # run algorithm
    # employees = algorithm(depot_coord, packages, employees)

    # write output
    # write_output(employees, file_output)

    return


assign('input.txt', 'output.txt')
