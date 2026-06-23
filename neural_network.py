"""
Neural Networks  (Images 1 & 2)
=================================
From notebook:
  - Input layer → Hidden layers → Output layer
  - Each neuron contributes to one input
  - Mapped with interests (weights)
  - Activation function applied
  - Highest weight input selected

Architecture shown in Image 2:
  Input layer  : 5 neurons
  Hidden layer1: 5 neurons
  Hidden layer2: 5 neurons
  Output layer : 4 neurons
"""

import numpy as np

# ──────────────────────────────────────────────
# 1.  Activation Functions
# ──────────────────────────────────────────────
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_derivative(z):
    s = sigmoid(z)
    return s * (1 - s)

def relu(z):
    return np.maximum(0, z)

def relu_derivative(z):
    return (z > 0).astype(float)

def softmax(z):
    e_z = np.exp(z - np.max(z))
    return e_z / e_z.sum(axis=0)

# ──────────────────────────────────────────────
# 2.  Neural Network Class
# ──────────────────────────────────────────────
class NeuralNetwork:
    """
    Fully connected neural network matching notebook diagram:
      Input(5) → Hidden1(5) → Hidden2(5) → Output(4)
    """

    def __init__(self, layer_sizes, activation='sigmoid', learning_rate=0.1):
        """
        layer_sizes : list of ints e.g. [5, 5, 5, 4]
        activation  : 'sigmoid' or 'relu'
        """
        self.layer_sizes   = layer_sizes
        self.lr            = learning_rate
        self.activation    = activation
        self.weights       = []   # W matrices
        self.biases        = []   # b vectors
        self.cache         = {}   # store Z, A for backprop

        self._initialize_weights()

    # ── Weight initialisation ──────────────────
    def _initialize_weights(self):
        np.random.seed(42)
        for i in range(len(self.layer_sizes) - 1):
            n_in  = self.layer_sizes[i]
            n_out = self.layer_sizes[i + 1]
            # Xavier initialisation
            W = np.random.randn(n_out, n_in) * np.sqrt(2.0 / n_in)
            b = np.zeros((n_out, 1))
            self.weights.append(W)
            self.biases.append(b)

    # ── Activation helper ─────────────────────
    def _activate(self, Z, output_layer=False):
        if output_layer:
            return sigmoid(Z)
        return relu(Z) if self.activation == 'relu' else sigmoid(Z)

    def _activate_deriv(self, Z):
        return relu_derivative(Z) if self.activation == 'relu' else sigmoid_derivative(Z)

    # ── Forward pass ──────────────────────────
    def forward(self, X):
        """
        X : (n_features, n_samples)
        Returns output A of final layer
        """
        A = X
        self.cache['A0'] = X

        for i, (W, b) in enumerate(zip(self.weights, self.biases)):
            Z = W @ A + b                          # linear step
            is_output = (i == len(self.weights) - 1)
            A = self._activate(Z, output_layer=is_output)

            self.cache[f'Z{i+1}'] = Z
            self.cache[f'A{i+1}'] = A

        return A

    # ── Loss (Binary Cross-Entropy) ───────────
    def compute_loss(self, Y_hat, Y):
        m = Y.shape[1]
        loss = -np.mean(Y * np.log(Y_hat + 1e-8) + (1 - Y) * np.log(1 - Y_hat + 1e-8))
        return loss

    # ── Backward pass ─────────────────────────
    def backward(self, X, Y):
        m = X.shape[1]
        L = len(self.weights)
        grads_W = [None] * L
        grads_b = [None] * L

        # Output layer gradient
        A_out = self.cache[f'A{L}']
        dA = -(Y / (A_out + 1e-8)) + ((1 - Y) / (1 - A_out + 1e-8))

        for i in reversed(range(L)):
            Z = self.cache[f'Z{i+1}']
            A_prev = self.cache[f'A{i}']
            is_output = (i == L - 1)

            dZ = dA * (sigmoid_derivative(Z) if is_output else self._activate_deriv(Z))
            grads_W[i] = (dZ @ A_prev.T) / m
            grads_b[i] = np.mean(dZ, axis=1, keepdims=True)
            dA = self.weights[i].T @ dZ

        # Update weights
        for i in range(L):
            self.weights[i] -= self.lr * grads_W[i]
            self.biases[i]  -= self.lr * grads_b[i]

    # ── Training ──────────────────────────────
    def train(self, X, Y, epochs=1000, print_every=100):
        print("=" * 55)
        print(f"NEURAL NETWORK TRAINING")
        print(f"  Architecture : {self.layer_sizes}")
        print(f"  Activation   : {self.activation}")
        print(f"  Learning rate: {self.lr}")
        print(f"  Epochs       : {epochs}")
        print("=" * 55)

        losses = []
        for epoch in range(1, epochs + 1):
            Y_hat = self.forward(X)
            loss  = self.compute_loss(Y_hat, Y)
            losses.append(loss)
            self.backward(X, Y)

            if epoch % print_every == 0 or epoch == 1:
                print(f"  Epoch {epoch:>5}  |  Loss = {loss:.6f}")

        print("=" * 55)
        return losses

    # ── Predict ───────────────────────────────
    def predict(self, X, threshold=0.5):
        Y_hat = self.forward(X)
        return (Y_hat >= threshold).astype(int)

    # ── Summary ───────────────────────────────
    def summary(self):
        print("\n📐 Network Summary:")
        total_params = 0
        for i, (W, b) in enumerate(zip(self.weights, self.biases)):
            params = W.size + b.size
            total_params += params
            print(f"  Layer {i+1}: {self.layer_sizes[i]} → {self.layer_sizes[i+1]}"
                  f"  |  W{W.shape}  b{b.shape}  |  params={params}")
        print(f"  Total parameters: {total_params}")


# ──────────────────────────────────────────────
# 3.  Main – XOR problem demo
# ──────────────────────────────────────────────
if __name__ == "__main__":
    # XOR dataset (classic non-linear problem)
    X = np.array([[0, 0, 1, 1],
                  [0, 1, 0, 1]])        # shape (2, 4)
    Y = np.array([[0, 1, 1, 0]])        # shape (1, 4)

    # Network matching notebook: Input→Hidden1→Hidden2→Output
    # For XOR: 2 inputs, two hidden layers of 4, 1 output
    nn = NeuralNetwork(layer_sizes=[2, 4, 4, 1],
                       activation='sigmoid',
                       learning_rate=0.5)
    nn.summary()

    losses = nn.train(X, Y, epochs=5000, print_every=500)

    preds = nn.predict(X)
    print(f"\nPredictions : {preds.flatten()}")
    print(f"Ground truth: {Y.flatten()}")
    accuracy = np.mean(preds == Y) * 100
    print(f"Accuracy    : {accuracy:.1f}%")

    # ── Larger network matching notebook diagram ──
    print("\n\n--- Notebook Architecture: 5→5→5→4 ---")
    np.random.seed(0)
    X_demo = np.random.randn(5, 10)      # 5 inputs, 10 samples
    Y_demo = (np.random.rand(4, 10) > 0.5).astype(float)

    nn2 = NeuralNetwork(layer_sizes=[5, 5, 5, 4],
                        activation='relu',
                        learning_rate=0.01)
    nn2.summary()
    nn2.train(X_demo, Y_demo, epochs=1000, print_every=200)
