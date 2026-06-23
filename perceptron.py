"""
Single Perceptron / Neuron  (Image 3)
=======================================
From notebook diagram:
  Inputs : x1, x2, ..., xn
  Weights: w1, w2, ..., wn
  Bias   : b
  Neuron : N  →  weighted sum
  Output : y = g(w·x + b)   where g = activation function

Formula:  y = g(w · x + b)

Types of neural networks mentioned:
  1. CNN
  2. RNN
  3. Others / Autoencoders
"""

import numpy as np

# ──────────────────────────────────────────────
# 1.  Activation functions for a single neuron
# ──────────────────────────────────────────────
def sigmoid(z):       return 1 / (1 + np.exp(-z))
def relu(z):          return max(0, z)
def step(z):          return 1 if z >= 0 else 0
def tanh_fn(z):       return np.tanh(z)

# ──────────────────────────────────────────────
# 2.  Single Perceptron Class
# ──────────────────────────────────────────────
class Perceptron:
    """
    Single neuron:  y = g(w · x + b)
    Matches the notebook diagram exactly.
    """

    def __init__(self, n_inputs, activation='sigmoid', learning_rate=0.1):
        np.random.seed(42)
        self.weights = np.random.randn(n_inputs)   # w1, w2, ..., wn
        self.bias    = 0.0                          # b
        self.lr      = learning_rate
        self.activation_name = activation

    # ── Activation ────────────────────────────
    def _activate(self, z):
        if self.activation_name == 'sigmoid':  return sigmoid(z)
        if self.activation_name == 'relu':     return relu(z)
        if self.activation_name == 'step':     return step(z)
        if self.activation_name == 'tanh':     return tanh_fn(z)
        return z

    # ── Forward  y = g(w·x + b) ───────────────
    def predict(self, x):
        """
        x : array of inputs [x1, x2, ..., xn]
        Returns output y
        """
        weighted_sum = np.dot(self.weights, x) + self.bias   # w·x + b
        y = self._activate(weighted_sum)
        return y

    # ── Perceptron Learning Rule ───────────────
    def train(self, X, Y, epochs=100):
        """
        X : list of input vectors
        Y : list of target outputs (0 or 1)
        """
        print("=" * 50)
        print("SINGLE PERCEPTRON TRAINING")
        print(f"  Inputs     : {len(self.weights)}")
        print(f"  Activation : {self.activation_name}")
        print(f"  LR         : {self.lr}")
        print("=" * 50)
        print(f"  Init weights : {self.weights.round(3)}")
        print(f"  Init bias    : {self.bias:.3f}")
        print("-" * 50)

        for epoch in range(1, epochs + 1):
            total_error = 0
            for x, target in zip(X, Y):
                output = self.predict(x)
                error  = target - output

                # Weight update:  w = w + lr * error * x
                self.weights += self.lr * error * np.array(x)
                self.bias    += self.lr * error

                total_error += abs(error)

            if epoch % 10 == 0 or epoch == 1:
                print(f"  Epoch {epoch:>4}  |  Total error = {total_error:.4f}"
                      f"  |  w = {self.weights.round(3)}  b = {self.bias:.3f}")

            if total_error == 0:
                print(f"\n  ✅ Converged at epoch {epoch}!")
                break

        print("=" * 50)

    # ── Show computation step-by-step ─────────
    def show_computation(self, x, label=""):
        print(f"\n{'─'*40}")
        print(f"Input : {x}  {label}")
        print(f"Weights: {self.weights.round(4)}")
        print(f"Bias   : {self.bias:.4f}")
        weighted_sum = np.dot(self.weights, x) + self.bias
        print(f"w·x + b = {weighted_sum:.4f}")
        y = self._activate(weighted_sum)
        print(f"g(w·x+b) = {self.activation_name}({weighted_sum:.4f}) = {y:.4f}")
        print(f"Output y = {y:.4f}  →  class = {1 if y >= 0.5 else 0}")
        return y


# ──────────────────────────────────────────────
# 3.  Main – AND gate demo
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("╔══════════════════════════════════════╗")
    print("║      SINGLE PERCEPTRON  (Neuron)     ║")
    print("║   y = g(w · x + b)                  ║")
    print("╚══════════════════════════════════════╝\n")

    # ── AND Gate ──────────────────────────────
    print("📌 Example 1: AND Gate  (2 inputs)")
    X_and = [[0,0], [0,1], [1,0], [1,1]]
    Y_and = [0,     0,     0,     1    ]

    p = Perceptron(n_inputs=2, activation='step', learning_rate=0.1)
    p.train(X_and, Y_and, epochs=100)

    print("\nFinal predictions (AND gate):")
    for x, y_true in zip(X_and, Y_and):
        y_pred = p.predict(x)
        status = '✅' if int(y_pred) == y_true else '❌'
        print(f"  x={x}  target={y_true}  predicted={int(y_pred)}  {status}")

    # ── Show computation for one input ────────
    p.show_computation([1, 1], label="(AND: 1 AND 1 = 1)")

    # ── OR Gate ───────────────────────────────
    print("\n\n📌 Example 2: OR Gate  (2 inputs)")
    X_or = [[0,0], [0,1], [1,0], [1,1]]
    Y_or = [0,     1,     1,     1    ]

    p2 = Perceptron(n_inputs=2, activation='step', learning_rate=0.1)
    p2.train(X_or, Y_or, epochs=100)

    print("\nFinal predictions (OR gate):")
    for x, y_true in zip(X_or, Y_or):
        y_pred = p2.predict(x)
        status = '✅' if int(y_pred) == y_true else '❌'
        print(f"  x={x}  target={y_true}  predicted={int(y_pred)}  {status}")

    # ── 3-input neuron (matching notebook xn) ─
    print("\n\n📌 Example 3: 3-input neuron (x1,x2,x3)")
    p3 = Perceptron(n_inputs=3, activation='sigmoid', learning_rate=0.1)
    p3.show_computation([1, 0.5, -1], label="(x1=1, x2=0.5, x3=-1)")
