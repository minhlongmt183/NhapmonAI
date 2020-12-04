from random import randint
upperBound = 20
res = lambda lower=0,upper=20: randint(lower,upper)

with open("input.txt","w") as file:
    file.write("{} {}\n".format(res(7,13),res(7,13)))
    package = res(1,100)
    shipper = res(1,80)
    while shipper >= package or shipper == 1:
        shipper =res(1)
    file.write("{} {}\n".format(package,shipper))
    for i in range(package):
        file.write(" ".join([str(res()) for i in range(4)]))
        file.write("\n")