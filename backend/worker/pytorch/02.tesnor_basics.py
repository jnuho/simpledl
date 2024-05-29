# %%
# Tensor Basics
import torch

x = torch.empty(2, 3)
print("empty:", x)

x = torch.rand(2, 3)
print("rand:", x)

x = torch.zeros(2, 3)
print("zeros:", x)

# dtype: int, double, float16
x = torch.ones(2, 3, dtype=torch.double)
print("ones(.., dtype=float16):", x)

x = torch.tensor([2.5, .1])
print(x)



# %%
import torch

x = torch.rand(2,2)
y = torch.rand(2,2)
z = x+y
print(z)
z = torch.add(x,y)
print(z)

# trailing underscore: in place operation (modity variable)
y.add_(x) # y = x + y
print(y)

z = x-y
z = torch.sub(x,y)
x.sub_(y) # x = x - y

z = x*y
z = torch.mul(x,y)
x.mul_(y) # x = x * y

z = x/y
z = torch.div(x,y)
x.div_(y) # x = x / y



# %%
import torch

# slicing
x = torch.rand(5, 3)
# first column
print(x[:, 0])

# first row
print(x[0, :])

# second row
print(x[1, :])

# element(1,1) as a tensor
print(x[1,1])
# element(1,1) as an actual value
print(x[1,1].item())



# %%
import torch

# reshape
x = torch.rand(4,4)
print(x)
y = x.view(16)
print(y)

# don't specify in first dimension, then pytorch determines for you
# torch.Size([2, 8])
y = x.view(-1, 8)
print(y.size())



# %%
# Convert between numpy <-> torch.tensor
import torch
import numpy as np

# 1. torch -> numpy
a = torch.ones(5)
print(a)
print(type(a))

b = a.numpy()
print(b)
print(type(b))

# if tensor is on CPU and not on GPU,
# object will be on the same location
# CHANGING `b` will also change `a` and vice versa!
a.add_(1)
print(a)
print(b)

# 2. numpy -> torch
a = np.ones(5)
print(a)
b = torch.from_numpy(a)
print(b)
a += 1
print(a)
print(b)

print(torch.cuda.is_available())

if torch.cuda.is_available():
    # Specify cuda device
    device = torch.device("cuda")
    # create tensor using GPU
    x = torch.ones(5, device=device)
    # or create first and then move it to your cuda device to make it use GPU
    y = torch.ones(5)
    y = y.to(device)

    # performed on GPU which is much faster
    z = x+y

    # ERORR: because numpy can only handle CPU tensor
    # z.numpy()

    # move it back to CPU
    z = z.to("cpu")



# %%
import torch
import numpy as np

# False by default
# pytorch would need to calculate gradient descent in the optimization step
x = torch.ones(5, requires_grad=True)
print(x)
