import memory_graph as mg
import matplotlib.pyplot as plt
import random
random.seed(0)

N = 100
value = 0
data = [value]
for i in range(N):
    value += random.uniform(-1, 1)
    data.append(value)
    
plt.plot(data)
plt.savefig('plot.png')
image = {mg.html_str('<IMG SRC="plot.png"/>')}

mg.render(locals(), 'html_str_image.png')

