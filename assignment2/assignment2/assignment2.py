# Them cac thu vien neu can

def assign(file_input, file_output):
    # read input

    with open(file_input, "r") as f:
        # get depot_coordinates
        depot_coordinates = f.readline().split(' ') 

        # get number employees and number packages
        data = f.readline().split(' ')
        number_packages = int(data[0])
        number_employees = int(data[1])

        # get infor of packages
        packages = []

        for i in range(number_packages):
            package = {}
            package_info = f.readline().split(' ')

            package["id"] = int(i)
            package["dest_coord_x"] = int(package_info[0])
            package["dest_coord_y"] = int(package_info[1])
            package["volume"] = int(package_info[2])
            package["weight"] = int(package_info[3])

            packages.append(package)
  

    # run algorithm
    # write output
    return


assign('input.txt', 'output.txt')
