import numpy as np

# Simple neural network model implementation
class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # initialize weights and biases
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
    
    def forward(self, X):
        # forward propagation
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = np.tanh(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = 1 / (1 + np.exp(-self.z2))  # sigmoid activation function
        return self.a2
    
    def backward(self, X, y, learning_rate=0.1):
        # backward propagation
        m = X.shape[0]
        
        # compute gradients
        dz2 = self.a2 - y
        dW2 = np.dot(self.a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m
        
        dz1 = np.dot(dz2, self.W2.T) * (1 - np.power(self.a1, 2))
        dW1 = np.dot(X.T, dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m
        
        # update parameters
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
    
    def compute_loss(self, y_pred, y_true):
        # compute binary cross-entropy loss
        m = y_true.shape[0]
        loss = -np.sum(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)) / m
        return loss

# generate some simple training data
np.random.seed(42)
X = np.random.randn(100, 2)  # 100 samples, 2 features each
y = np.array((X[:, 0] + X[:, 1]) > 0).reshape(-1, 1).astype(np.float64)  # simple classification task

# create model
model = SimpleNeuralNetwork(input_size=2, hidden_size=3, output_size=1)

# train model
print("Starting model training...")
for epoch in range(10):
    # forward pass
    y_pred = model.forward(X)
    
    # compute loss
    loss = model.compute_loss(y_pred, y)
    
    # backward pass
    model.backward(X, y)
    
    # print training progress
    print(f"Epoch {epoch+1}/10, Loss: {loss:.4f}")

# test model
test_X = np.array([[0.5, 0.5], [-0.5, -0.5], [0.5, -0.5], [-0.5, 0.5]])
predictions = model.forward(test_X)
print("\nTest results:")
for i, pred in enumerate(predictions):
    print(f"Sample {i+1}: Input = {test_X[i]}, Prediction = {pred[0]:.4f}, Actual = {float((test_X[i, 0] + test_X[i, 1]) > 0)}")