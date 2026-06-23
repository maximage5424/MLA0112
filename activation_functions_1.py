"""
Activation Functions  –  ReLU & Others  (Image 4)
===================================================
From notebook:
  ReLU = Rectified Linear Unit
  "It is the mostly used activation function
   because it predicts from 0 to ∞,
   and also it can handle the inputs with
   negative values."

  Graph shown: x-axis [-10 to 10], y-axis [0 to 10]
  ReLU: f(x) = max(0, x)

Also implements all common activation functions
for comparison.
"""

import numpy as np
import matplotlib.pyplot as plt

# ──────────────────────────────────────────────
# 1.  All Activation Functions
# ──────────────────────────────────────────────
def relu(x):
    """ReLU: f(x) = max(0, x)  — notebook Image 4"""
    return np.maximum(0, x)

def leaky_relu(x, alpha=0.01):
    """Leaky ReLU: handles dying neuron problem"""
    return np.where(x > 0, x, alpha * x)

def sigmoid(x):
    """Sigmoid: f(x) = 1 / (1 + e^-x)"""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def tanh(x):
    """Tanh: f(x) = (e^x - e^-x) / (e^x + e^-x)"""
    return np.tanh(x)

def step(x):
    """Step / Heaviside: f(x) = 1 if x>=0 else 0"""
    return np.where(x >= 0, 1.0, 0.0)

def linear(x):
    """Linear: f(x) = x"""
    return x

def softmax(x):
    """Softmax for a 1D array"""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

# ── Derivatives ───────────────────────────────
def relu_deriv(x):        return np.where(x > 0, 1.0, 0.0)
def sigmoid_deriv(x):     s = sigmoid(x); return s * (1 - s)
def tanh_deriv(x):        return 1 - np.tanh(x)**2

# ──────────────────────────────────────────────
# 2.  Plot all activation functions
# ──────────────────────────────────────────────
def plot_activation_functions():
    x = np.linspace(-10, 10, 400)

    functions = {
        'ReLU\nf(x)=max(0,x)':          relu(x),
        'Sigmoid\nf(x)=1/(1+e⁻ˣ)':      sigmoid(x),
        'Tanh\nf(x)=tanh(x)':           tanh(x),
        'Step\nf(x)=0 or 1':            step(x),
        'Leaky ReLU\nf(x)=max(0.01x,x)': leaky_relu(x),
        'Linear\nf(x)=x':               linear(x),
    }

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    fig.suptitle('Activation Functions (Neural Networks)', fontsize=16, fontweight='bold')

    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#f39c12', '#1abc9c']

    for ax, (name, y), color in zip(axes.flatten(), functions.items(), colors):
        ax.plot(x, y, color=color, linewidth=2.5)
        ax.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
        ax.axvline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
        ax.set_title(name, fontsize=11, fontweight='bold')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-10, 10)

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/activation_functions.png', dpi=150, bbox_inches='tight')
    print("  ✅ Saved: activation_functions.png")
    plt.show()

# ──────────────────────────────────────────────
# 3.  Plot ReLU specifically (as in notebook)
# ──────────────────────────────────────────────
def plot_relu():
    x = np.linspace(-10, 10, 400)
    y = relu(x)
    y_deriv = relu_deriv(x)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('ReLU – Rectified Linear Unit', fontsize=14, fontweight='bold')

    # ReLU
    ax1.plot(x, y, color='#e74c3c', linewidth=3, label='ReLU: f(x) = max(0, x)')
    ax1.fill_between(x, 0, y, alpha=0.15, color='#e74c3c')
    ax1.axhline(0, color='black', linewidth=0.8)
    ax1.axvline(0, color='black', linewidth=0.8)
    ax1.set_title('ReLU Function\n(as shown in notebook)', fontsize=12)
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.set_xlim(-10, 10)
    ax1.set_ylim(-1, 11)
    ax1.set_yticks([0, 2, 4, 6, 8, 10])
    ax1.set_xticks([-10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10])
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    # Annotations
    ax1.annotate('Negative input → 0\n(handles negatives!)',
                 xy=(-5, 0), xytext=(-9, 3),
                 arrowprops=dict(arrowstyle='->', color='gray'),
                 fontsize=9, color='navy')
    ax1.annotate('Positive input → x\n(0 to ∞)',
                 xy=(5, 5), xytext=(2, 8),
                 arrowprops=dict(arrowstyle='->', color='gray'),
                 fontsize=9, color='navy')

    # Derivative
    ax2.plot(x, y_deriv, color='#3498db', linewidth=3,
             label="ReLU': 0 if x<0, 1 if x>0")
    ax2.set_title("ReLU Derivative", fontsize=12)
    ax2.set_xlabel('x')
    ax2.set_ylabel("f'(x)")
    ax2.set_xlim(-10, 10)
    ax2.set_ylim(-0.2, 1.5)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/relu_plot.png', dpi=150, bbox_inches='tight')
    print("  ✅ Saved: relu_plot.png")
    plt.show()

# ──────────────────────────────────────────────
# 4.  Numerical demonstration
# ──────────────────────────────────────────────
def demo_activations():
    print("=" * 55)
    print("ACTIVATION FUNCTIONS  –  Numerical Demo")
    print("=" * 55)

    test_values = [-5, -2, -1, 0, 1, 2, 5]
    print(f"\n{'x':>6} | {'ReLU':>8} | {'Sigmoid':>8} | {'Tanh':>8} | {'Step':>6}")
    print("-" * 50)
    for xv in test_values:
        print(f"{xv:>6} | {relu(np.array([xv]))[0]:>8.4f} | "
              f"{sigmoid(np.array([xv]))[0]:>8.4f} | "
              f"{tanh(np.array([xv]))[0]:>8.4f} | "
              f"{step(np.array([xv]))[0]:>6.0f}")

    print("\n📌 ReLU Key Properties:")
    print("  f(x) = max(0, x)")
    print("  • Output range: [0, ∞)")
    print("  • Derivative  : 0 for x<0,  1 for x>0")
    print("  • Most used: simple, efficient, no vanishing gradient for x>0")
    print("  • Handles negative inputs by outputting 0")
    print("=" * 55)

# ──────────────────────────────────────────────
# 5.  Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║    ACTIVATION FUNCTIONS  –  ReLU etc.   ║")
    print("╚══════════════════════════════════════════╝\n")

    demo_activations()

    print("\n📊 Plotting ReLU (as in notebook)...")
    plot_relu()

    print("\n📊 Plotting all activation functions...")
    plot_activation_functions()
