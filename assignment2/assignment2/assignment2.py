# Them cac thu vien neu can

def read_input(file_input):
    with open(file_input, "r") as f:
        # get depot_coordinates
        depot_coordinates = f.readline().split(' ') 

        # get number employees and number packages
        data = f.readline().split(' ')
        number_packages = int(data[0])
        number_employees = int(data[1])

        # get infor of packages
        packages = [None]*number_packages
        employees = [None]*number_employees

        for i in range(number_packages):
            package = {}
            package_info = f.readline().split(' ')

            package["id"] = int(i)
            package["dest_coord_x"] = int(package_info[0])
            package["dest_coord_y"] = int(package_info[1])
            package["volume"] = int(package_info[2])
            package["weight"] = int(package_info[3])

            packages.append(package)
        
    return depot_coordinates, packages, employees

def write_output(employees,file_output):
    with open(file_output, "w") as f:
        for employee in employees:
            for package in employee:
                f.write("{} ".format(package))
            f.write("\n")

def assign(file_input, file_output):
    # read input
    # depot_coordinates, packages, employees = read_input(file_input)


    # run algorithm


    
    # write output
    write_output(employees, file_output)

    return


assign('input.txt', 'output.txt')
