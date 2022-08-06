

x = 3000 
r = 0.09

y = 30
m = 32 * 12
c = 0

for i in range(1, m + 1):
    c = (c + x) * (1 + r/12)
    if i % 12 == 0:
        print("year: {}, return: {}".format(int(i/12), round(c, 2)))


 
