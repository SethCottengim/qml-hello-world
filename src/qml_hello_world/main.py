import pennylane as qml
from pennylane import numpy as np

# 1. Define the Device
# 'default.qubit' is a simple state simulator provided by PennyLane.
# wires=1 means we are using a single qubit.
dev = qml.device("default.qubit", wires=1)

# 2. Define the Quantum Node (The "Circuit")
# The @qml.qnode decorator links the quantum function to the device.
@qml.qnode(dev)
def circuit(params):
    # These rotations are the "weights" of our quantum neuron.
    # We are trying to find the perfect angles to flip the qubit.
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=0)
    
    # We measure the Expectation Value of the Pauli Z operator.
    # For state |0> (North Pole), result is 1.
    # For state |1> (South Pole), result is -1.
    return qml.expval(qml.PauliZ(0))

# 3. Define the Cost Function
# We want the circuit to output -1 (State |1>).
# So, we just treat the output as the cost. Minimizing it pushes it towards -1.
def cost(x):
    return circuit(x)

# 4. Initialize Parameters (Random weights)
init_params = np.array([0.011, 0.012], requires_grad=True)
print(f"Initial rotation angles: {init_params}")
print(f"Initial cost (expecting close to 1): {cost(init_params):.4f}")

# 5. The Optimization Loop (Standard ML)
# We use a standard Gradient Descent Optimizer
opt = qml.GradientDescentOptimizer(stepsize=0.4)
steps = 100
params = init_params

print("\n--- Training Start ---")
for i in range(steps):
    # Update parameters
    params = opt.step(cost, params)

    if (i + 1) % 20 == 0:
        print(f"Step {i+1:3d}: Cost = {cost(params):.4f} (Params: {params})")

print("\n--- Training Complete ---")
print(f"Final Angles: {params}")
print(f"Final State Value: {cost(params):.4f} (Close to -1 means success!)")