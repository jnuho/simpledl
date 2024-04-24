# %%
import time
import numpy as np
import h5py
import matplotlib.pyplot as plt
import scipy
from PIL import Image
from scipy import ndimage
import os
import imageio.v3 as iio
from skimage.transform import resize
# from dnn_app_utils_v3 import *

# %matplotlib inline
plt.rcParams['figure.figsize'] = (5.0, 4.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# %load_ext autoreload
# %autoreload 2

# np.random.seed(1)


def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    train_dataset_path = os.path.join(base_path, 'datasets/train_catvnoncat.h5')
    train_dataset = h5py.File(train_dataset_path, "r")
    # train_dataset = h5py.File('datasets/train_catvnoncat.h5', "r")
    train_set_x_orig = np.array(train_dataset["train_set_x"][:]) # your train set features
    train_set_y_orig = np.array(train_dataset["train_set_y"][:]) # your train set labels

    test_dataset_path = os.path.join(base_path, 'datasets/test_catvnoncat.h5')
    test_dataset = h5py.File(test_dataset_path, "r")
    # test_dataset = h5py.File('datasets/test_catvnoncat.h5', "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:]) # your test set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:]) # your test set labels

    classes = np.array(test_dataset["list_classes"][:]) # the list of classes
    
    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))
    
    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes


def initialize_parameters_deep(layers_dims):
    """
    layers_dims: L+1 layers including A^[0] = X, input feature
    """
    # np.random.seed(1)

    parameters = {}
    L = len(layers_dims)

    for l in range(1, L):
        parameters["W" + str(l)] = np.random.randn(layers_dims[l], layers_dims[l-1])/np.sqrt(layers_dims[l-1])
        parameters["b" + str(l)] = np.zeros((layers_dims[l], 1))

        assert(parameters["W" + str(l)].shape == (layers_dims[l], layers_dims[l-1]))
        assert(parameters["b" + str(l)].shape == (layers_dims[l], 1))

    return parameters


def linear_forward(A, W, b):
    Z = np.dot(W, A) + b

    assert(Z.shape == (W.shape[0], A.shape[1]))
    cache = (A, W, b)

    return Z, cache


def relu(Z):
    A = np.maximum(0, Z)
    cache = Z
    assert(A.shape == Z.shape)

    return A, cache


def sigmoid(Z):
    A = 1/(1+np.exp(-Z))
    cache = Z
    assert(A.shape == Z.shape)

    return A, cache


def linear_activation_forward(A_prev, W, b, activation):
    if activation == "relu":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = relu(Z)
    elif activation == "sigmoid":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = sigmoid(Z)

    cache = (linear_cache, activation_cache)

    assert(A.shape == (W.shape[0], A_prev.shape[1]))

    return A, cache


def L_model_forward(X, parameters):

    caches = []
    A = X
    L = len(parameters) // 2

    for l in range(1, L):
        A_prev = A
        A, cache = linear_activation_forward(A_prev,
                                             parameters["W"+str(l)],
                                             parameters["b"+str(l)],
                                             activation="relu")
        caches.append(cache)

    AL, cache = linear_activation_forward(A,
                                            parameters["W"+str(L)],
                                            parameters["b"+str(L)],
                                            activation="sigmoid")

    caches.append(cache)

    assert(AL.shape == (1, X.shape[1]))

    return AL, caches


def compute_cost(AL, Y):
    m = Y.shape[1]
    cost = 1/m * (-np.dot(Y, np.log(AL).T) - np.dot(1-Y, np.log(1-AL).T))

    # e.g.  [[17]] -> 17
    cost = np.squeeze(cost)

    assert(cost.shape == ())

    return cost


def relu_backward(dA, activation_cache):
    Z = activation_cache
    dZ = np.array(dA, copy=True)

    dZ[Z <= 0] = 0

    assert(dZ.shape == Z.shape)

    return dZ


def sigmoid_backward(dA, activation_cache):
    Z = activation_cache

    s = 1/(1 + np.exp(-Z))
    dZ = dA * s * (1-s)

    assert(dZ.shape == Z.shape)

    return dZ


def linear_backward(dZ, cache):
    A_prev, W, b = cache
    m = A_prev.shape[1]

    dW = 1/m * np.dot(dZ, A_prev.T)
    db = 1/m * np.sum(dZ, axis=1, keepdims=True)
    dA_prev = np.dot(W.T, dZ)

    return dA_prev, dW, db


def linear_activation_backward(dA, cache, activation):
    linear_cache, activation_cache = cache

    if activation == "sigmoid":
        dZ = sigmoid_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
    elif activation == "relu":
        dZ = relu_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)

    return dA_prev, dW, db


def L_model_backward(AL, Y, caches):
    grads = {}
    L = len(caches)
    m = AL.shape[1]
    Y = Y.reshape(AL.shape)

    # L = -YlogA - (1-Y)log(1-A)
    dAL = -(np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))

    current_cache = caches[L-1]
    grads["dA"+str(L-1)], grads["dW"+str(L)], grads["db"+str(L)] = linear_activation_backward(dAL, current_cache, activation="sigmoid")

    for l in reversed(range(L-1)):
        current_cache = caches[l]
        
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA"+str(l+1)], current_cache, activation="relu")

        grads["dA"+str(l)] = dA_prev_temp
        grads["dW"+str(l+1)] = dW_temp
        grads["db"+str(l+1)] = db_temp

    return grads


def update_parameters(parameters, grads, learning_rate):
    L = len(parameters) // 2

    # l = 0,1, ... L-1
    for l in range(L):
        parameters["W" + str(l+1)] = parameters["W" + str(l+1)] - learning_rate * grads["dW" + str(l+1)]
        parameters["b" + str(l+1)] = parameters["b" + str(l+1)] - learning_rate * grads["db" + str(l+1)]

    return parameters


def L_layer_model(X, Y, layers_dims, learning_rate = 0.0075, num_iterations = 3000, print_cost=False):#lr was 0.009
    """
    Implements a L-layer neural network: [LINEAR->RELU]*(L-1)->LINEAR->SIGMOID.
    
    Arguments:
    X -- data, numpy array of shape (number of examples, num_px * num_px * 3)
    Y -- true "label" vector (containing 0 if cat, 1 if non-cat), of shape (1, number of examples)
    layers_dims -- list containing the input size and each layer size, of length (number of layers + 1).
    learning_rate -- learning rate of the gradient descent update rule
    num_iterations -- number of iterations of the optimization loop
    print_cost -- if True, it prints the cost every 100 steps
    
    Returns:
    parameters -- parameters learnt by the model. They can then be used to predict.
    """

    # np.random.seed(1)
    costs = []                         # keep track of cost
    
    # Parameters initialization. (≈ 1 line of code)
    ### START CODE HERE ###
    parameters = initialize_parameters_deep(layers_dims)
    ### END CODE HERE ###
    
    # Loop (gradient descent)
    for i in range(0, num_iterations):

        # Forward propagation: [LINEAR -> RELU]*(L-1) -> LINEAR -> SIGMOID.
        ### START CODE HERE ### (≈ 1 line of code)
        AL, caches = L_model_forward(X, parameters)
        ### END CODE HERE ###
        
        # Compute cost.
        ### START CODE HERE ### (≈ 1 line of code)
        cost = compute_cost(AL, Y)
        ### END CODE HERE ###
    
        # Backward propagation.
        ### START CODE HERE ### (≈ 1 line of code)
        grads = L_model_backward(AL, Y, caches)
        ### END CODE HERE ###
 
        # Update parameters.
        ### START CODE HERE ### (≈ 1 line of code)
        parameters = update_parameters(parameters, grads, learning_rate)
        ### END CODE HERE ###
                
        # Print the cost every 100 training example
        if print_cost and i % 100 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)
            
    # plot the cost
    plt.plot(np.squeeze(costs))
    plt.ylabel('cost')
    plt.xlabel('iterations (per tens)')
    plt.title("Learning rate =" + str(learning_rate))
    plt.show()
    
    return parameters


def predict(X, y, parameters):
    """
    This function is used to predict the results of a  L-layer neural network.
    
    Arguments:
    X -- data set of examples you would like to label
    parameters -- parameters of the trained model
    
    Returns:
    p -- predictions for the given dataset X
    """
    
    m = X.shape[1]
    n = len(parameters) // 2 # number of layers in the neural network
    p = np.zeros((1,m))
    
    # Forward propagation
    probas, caches = L_model_forward(X, parameters)
    # print(probas)
    
    # convert probas to 0/1 predictions
    for i in range(0, probas.shape[1]):
        if probas[0,i] > 0.5:
            p[0,i] = 1
        else:
            p[0,i] = 0
    
    #print results
    # print ("predictions: " + str(p))
    # print ("true labels: " + str(y)
    print("Accuracy: "  + str(np.sum((p == y)/m)))
        
    return p


def convert_to_matrix(x, y, image_dir, num_px, my_label_y, offset):
    # Get a list of all files in the directory
    image_files = os.listdir(image_dir)

    # Filter the list for files ending with '.jpg' and starting with '0000000'
    image_files = [f for f in image_files if f.endswith('.jpg')]

    # Iterate over the image files
    for i, image_file in enumerate(image_files):
        # Full path to the image file
        fname = os.path.join(image_dir, image_file)
        
        # Read and preprocess the image
        image = np.array(iio.imread(fname))
        my_image = resize(image, (num_px, num_px)).reshape((num_px*num_px*3,1))
        my_image = my_image/255.

        x[:, i+offset] = my_image.flatten()
        y[:, i+offset] = my_label_y

    return x, y


def load_test_x_and_y():
    """
    return
    'test_x' (12288, 100) where 50 is non-cat
    'test_y' (1, 100)
    """
    num_px = 64

    test_x = np.zeros((num_px * num_px * 3, 100))
    test_y = np.zeros((1, 100))

    test_x, test_y = convert_to_matrix(test_x, test_y, "images/test/cat/", num_px, my_label_y=1, offset=0)
    test_x, test_y = convert_to_matrix(test_x, test_y, "images/test/noncat/", num_px, my_label_y=0, offset=50)

    return test_x, test_y

def load_train_x_and_y():
    """
    return
    'train_x' (12288, 400) where 200 is non-cat
    'train_y' (1, 400)
    """
    num_px = 64

    train_x = np.zeros((num_px * num_px * 3, 400))
    train_y = np.zeros((1, 400))

    train_x, train_y = convert_to_matrix(train_x, train_y, "images/train/cat/", num_px, my_label_y=1, offset=0)
    train_x, train_y = convert_to_matrix(train_x, train_y, "images/train/noncat/", num_px, my_label_y=0, offset=200)

    return train_x, train_y

def test_image(my_image, my_label_y):
    _, _, _, _, classes = load_data()

    #DeprecationWarning: Starting with ImageIO v3 the behavior of this function will switch to that of iio.v3.imread. To keep the current behavior (and make this warning disappear) use `import imageio.v2 as imageio` or call `imageio.v2.imread` directly.
    num_px = 64
    ## START CODE HERE ##
    # base_path = os.path.dirname(os.path.abspath(__file__))
    # my_image = os.path.join(base_path, 'cats/cat_body')
    # my_image = "cats/cat_body.jpg" # change this to the name of your image file
    # my_image = "my_image.jpg" # change this to the name of your image file
    my_label_y = [my_label_y] # the true class of your image (1 -> cat, 0 -> non-cat)
    ## END CODE HERE ##

    fname = "images/" + my_image
    # fname = "images/" + "weird_cat.jpg"
    # image = np.array(ndimage.imread(fname, flatten=False))
    image = np.array(iio.imread(fname))
    # my_image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((num_px*num_px*3,1))
    my_image = resize(image, (num_px, num_px)).reshape((num_px*num_px*3,1))
    # my_image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((num_px*num_px*3,1))
    my_image = my_image/255.

    my_predicted_image = predict(my_image, my_label_y, parameters)

    plt.imshow(image)
    print ("y = " + str(np.squeeze(my_predicted_image)) + ", your L-layer model predicts a \"" + classes[int(np.squeeze(my_predicted_image)),].decode("utf-8") +  "\" picture.")



def resize_image():
    # Use the function to resize your image
    image_dirs = ["images/test/cat",
                  "images/test/noncat",
                  "images/train/cat",
                  "images/train/noncat"]
    # Get a list of all files in the directory

    for image_dir in image_dirs:
        image_files = os.listdir(image_dir)

        # Filter the list for files ending with '.jpg' and starting with '0000000'
        image_files = [f for f in image_files if f.endswith('.jpg')]

        # Iterate over the image files
        for image_file in image_files:
            # Full path to the image file
            fname = os.path.join(image_dir, image_file)
            input_image_path = fname
            output_image_path = fname

            size = (64, 64)

            original_image = Image.open(input_image_path)
            width, height = original_image.size
            print(f"The original image size is {width} wide x {height} tall")

            resized_image = original_image.resize(size)
            width, height = resized_image.size
            print(f"The resized image size is {width} wide x {height} tall")
            # resized_image.show()

            # Save the resized image to the output path
            resized_image.save(output_image_path)


def preprocess_images(x):
    mean = x.mean(axis=0)
    std_dev = x.std(axis=0)
    x = (x - mean) / std_dev
    return x


# %%
# train_x_orig, train_y, test_x_orig, test_y, classes = load_data()
# train_x = train_x_orig.reshape(train_x_orig.shape[0], -1).T
# train_x = train_x / 255
# test_x = test_x_orig.reshape(test_x_orig.shape[0], -1).T
# test_x = test_x / 255

train_x, train_y = load_train_x_and_y()
test_x, test_y = load_test_x_and_y()

train_x = preprocess_images(train_x)
test_x = preprocess_images(test_x)

# %%
print(train_x.shape)
print(train_y.shape)

print(test_x.shape)
print(test_y.shape)


# %%
# L = 4 excluding the input feature X in layer [0]
# [12288, 20, 7, 5, 1]
# np.random.seed(1)
# layers_dims = [train_x.shape[0], 20, 7, 5, 1]
layers_dims = [train_x.shape[0], 20, 7, 1]

parameters = L_layer_model(train_x, train_y, layers_dims, learning_rate=.0075, num_iterations=2500, print_cost=True)


# %%
pred_train = predict(train_x, train_y, parameters)
pred_test = predict(test_x, test_y, parameters)


# %%

### Example of a picture ###
# train_x_orig, train_y_orig, test_x_orig, test_y_orig, classes = load_data()

# Standardize data to have feature values between 0 and 1.
# index = 16
# plt.imshow(test_x_orig[index])
# print ("y = " + str(test_y_orig[0,index]) + ". It's a " + classes[test_y_orig[0,index]].decode("utf-8") +  " picture.")
# my_predicted_image = predict(test_x[:,index].reshape(12288,1), [test_y_orig[0,index]], parameters)
# print ("y = " + str(np.squeeze(my_predicted_image)) + ", your L-layer model predicts a \"" + classes[int(np.squeeze(my_predicted_image)),].decode("utf-8") +  "\" picture.")

# test_image("cat_body.jpg", 1)
test_image("my_image.jpg", 1)
# test_image("weird_cat.jpg", 1)
# test_image("gargouille.jpg", 1)
# test_image("test/cat/00000001_000.jpg", 1)
# test_image("test/noncat/horse-60.jpg", 0)
test_image("train/cat/cat.99.jpg", 1)



