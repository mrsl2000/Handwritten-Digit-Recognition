import numpy as np
import random
import matplotlib.pyplot as plt

# functions

def max_index(m):
    tmp = None
    index = None

    for i in range(m.size):
        if tmp is None:
            tmp = m[i][0]
            index = i

        elif m[i][0] > tmp:
            tmp = m[i][0]
            index = i

    return index

def sigmoid(x):
    return (np.tanh(x))       

def sigmoid_derivative(x):
    return 1/ np.cosh(x) ** 2


# *************************************** Begining of first part ***************************************


# A function to plot images
def show_image(img):
    image = img.reshape((28, 28))
    plt.imshow(image, 'gray')


# Reading The Train Set
train_images_file = open('train-images.idx3-ubyte', 'rb')
train_images_file.seek(4)
num_of_train_images = int.from_bytes(train_images_file.read(4), 'big')
train_images_file.seek(16)

train_labels_file = open('train-labels.idx1-ubyte', 'rb')
train_labels_file.seek(8)

train_set = []
for n in range(num_of_train_images):
    image = np.zeros((784, 1))
    for i in range(784):
        image[i, 0] = int.from_bytes(train_images_file.read(1), 'big') / 256

    label_value = int.from_bytes(train_labels_file.read(1), 'big')
    label = np.zeros((10, 1))
    label[label_value, 0] = 1
    
    train_set.append((image, label))


# Reading The Test Set
test_images_file = open('t10k-images.idx3-ubyte', 'rb')
test_images_file.seek(4)

test_labels_file = open('t10k-labels.idx1-ubyte', 'rb')
test_labels_file.seek(8)

num_of_test_images = int.from_bytes(test_images_file.read(4), 'big')
test_images_file.seek(16)

test_set = []
for n in range(num_of_test_images):
    image = np.zeros((784, 1))
    for i in range(784):
        image[i] = int.from_bytes(test_images_file.read(1), 'big') / 256
    
    label_value = int.from_bytes(test_labels_file.read(1), 'big')
    label = np.zeros((10, 1))
    label[label_value, 0] = 1
    
    test_set.append((image, label))


# # Plotting an image
# show_image(train_set[0][0])
# plt.show()


# *************************************** End of first part ***************************************

# *************************************** Begining of seventh part ***************************************
# Calculate cost_function
cost_function = []

# random weights and biases
weight1 = np.random.randn(16,784)
weight2 = np.random.randn(16,16)
weight3 = np.random.randn(10,16)
bias1 = np.zeros((16,1))
bias2 = np.zeros((16,1))
bias3 = np.zeros((10,1))

# Initialize parameters
learning_rate = 1
num_epochs = 5
batch_size = 50

for i in range(num_epochs):
    cost = 0
    random.shuffle(train_set)
    for j in range(int(num_of_train_images/batch_size)):

        grad_w1 = np.zeros((16,784))
        grad_w2 = np.zeros((16,16))
        grad_w3 = np.zeros((10,16))

        grad_b1 = np.zeros((16,1))
        grad_b2 = np.zeros((16,1))
        grad_b3 = np.zeros((10,1))

        grad_a1 = np.zeros((16,1))
        grad_a2 = np.zeros((16,1))


        for k in range((j-1)*batch_size,j*batch_size):

            z1 = ((weight1 @ train_set[k][0]) + bias1)
            a1 = sigmoid(z1)

            z2 = ((weight2 @ a1) + bias2)
            a2 = sigmoid(z2)

            z3 = ((weight3 @ a2) + bias3)
            a3 = sigmoid(z3)
            
            
            for l in range(a3.size):
                cost += (a3[l] - train_set[k][1][l]) ** 2
                
            
# w3 , b3 , a2

            grad_w3 += (sigmoid_derivative(z3) * (2 * a3 - 2 * train_set[k][1])) @ (np.transpose(a2)) 

            grad_b3 += (sigmoid_derivative(z3) * (2 * a3 - 2 * train_set[k][1])) 

            grad_a2 =  (np.transpose(weight3) @ (sigmoid_derivative(z3) * (2 * a3 - 2 * train_set[k][1])))

# w2 , b2 , a1

            grad_w2 += (sigmoid_derivative(z2) * grad_a2) @ (np.transpose(a1)) 

            grad_b2 += (sigmoid_derivative(z2) * grad_a2)

            grad_a1 = (np.transpose(weight2) @ (sigmoid_derivative(z2) * grad_a2))


# w1 , b1 

            grad_w1 += (sigmoid_derivative(z1) * grad_a1) @ (np.transpose(train_set[k][0])) 

            grad_b1 += (sigmoid_derivative(z1) * grad_a1)


        
        weight1 -= learning_rate * (grad_w1/batch_size)
        weight2 -= learning_rate * (grad_w2/batch_size)
        weight3 -= learning_rate * (grad_w3/batch_size)
        bias1 -= learning_rate * (grad_b1/batch_size)
        bias2 -= learning_rate * (grad_b2/batch_size)
        bias3 -= learning_rate * (grad_b3/batch_size)    

    cost_function.append((cost/num_of_train_images))


# Accuracy calculator
count = 0
for i in range(num_of_test_images):

    a1 = sigmoid((weight1 @ test_set[i][0]) + bias1)
    a2 = sigmoid((weight2 @ a1) + bias2)
    a3 = sigmoid((weight3 @ a2) + bias3)
    
    guess = max_index(a3)
    final = max_index(test_set[i][1])
    
    if guess == final:
        count += 1
    
print(" Accuracy of test set: " + str(count/num_of_test_images * 100) )

count = 0
for i in range(num_of_train_images):

    a1 = sigmoid((weight1 @ train_set[i][0]) + bias1)
    a2 = sigmoid((weight2 @ a1) + bias2)
    a3 = sigmoid((weight3 @ a2) + bias3)
    
    guess = max_index(a3)
    final = max_index(train_set[i][1])
    
    if guess == final:
        count += 1
    
print(" Accuracy for training set: " + str(count/num_of_train_images * 100) )


plt.plot(cost_function)
plt.show()

# *************************************** End of seventh part ***************************************