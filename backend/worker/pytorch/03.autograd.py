# %%
# Calculate gradients using autograd pacakge
import torch

# in order to calculate gradient with respect to x later
x = torch.randn(3, requires_grad=True)
print(x)

# input: x,2, output: y
# Forward propagation
# pytorch creates and stores a function that calculates gradient descent
# gradient of y with respect to x
y = x + 2
print(y) ## AddBackward
z = y*y*2
print(z) ## MulBackward
# z = z.mean()
print(z) ## MeanBackward

v = torch.tensor([.1, 1.0, .001], dtype=torch.float32)
z.backward(v) # dz/dx

# Calculate the Jacobian matrix for the vector-valued function
# Here we assume the function is the gradient of z with respect to x
# which has already been computed as x.grad after z.backward()

# Since z is a scalar, the Jacobian of z with respect to x is simply the gradient itself
# which has been computed and stored in x.grad
jacobian_matrix = x.grad
print("Jacobian matrix of z with respect to x:")
print(jacobian_matrix)

