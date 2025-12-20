import os
import re
import sys

import matplotlib.pyplot as plt
import pandas as pd

python_env = sys.executable
print(f"Python executable: {python_env}")

# Path to the log file
log_file_path = os.path.join(os.path.dirname(__file__), "..", "logs", "training.log")

try:
    with open(log_file_path, "r") as f:
        log_data = f.read()
except FileNotFoundError:
    print(f"Error: Log file not found at {log_file_path}")
    exit(1)


epochs = []
losses = []
accuracies = []

epoch_pattern = re.compile(r"epoch: (\d+)")
loss_pattern = re.compile(r"\[\d+\] loss: ([\d.]+)")
acc_pattern = re.compile(r"Accuracy of the network on the val images: (\d+) %")

lines = log_data.split("\n")
current_epoch = None
current_loss = None

for line in lines:
    epoch_match = epoch_pattern.search(line)
    if epoch_match:
        current_epoch = int(epoch_match.group(1))

    loss_match = loss_pattern.search(line)
    if loss_match:
        current_loss = float(loss_match.group(1))

    acc_match = acc_pattern.search(line)
    if acc_match:
        current_acc = int(acc_match.group(1))
        if current_epoch is not None and current_loss is not None:
            epochs.append(current_epoch + 1)
            losses.append(current_loss)
            accuracies.append(current_acc)

df = pd.DataFrame({"Epoch": epochs, "Loss": losses, "Accuracy": accuracies})

# --- Plotting with new style and separate plots ---

# Set style to default to match the requested style (white background, etc.)
plt.style.use("default")

# Create figure and subplots (2 rows, 1 column)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))  # Increased height for two plots

# --- Plot 1: Training Loss ---
# Scatter plot for data points (blue circles)
ax1.scatter(df["Epoch"], df["Loss"], color="blue", label="Training Loss Points")
# Line plot for the trend (red line)
ax1.plot(df["Epoch"], df["Loss"], color="red", label="Loss Trend")

ax1.set_title("Training Loss")
ax1.set_ylabel("Loss")
ax1.set_xlabel("Epoch")
ax1.grid(True)
ax1.legend()  # Add legend

# --- Plot 2: Validation Accuracy ---
# Scatter plot for data points (blue circles)
ax2.scatter(
    df["Epoch"], df["Accuracy"], color="blue", label="Validation Accuracy Points"
)
# Line plot for the trend (red line)
ax2.plot(df["Epoch"], df["Accuracy"], color="red", label="Accuracy Trend")

ax2.set_title("Validation Accuracy")
ax2.set_ylabel("Accuracy (%)")
ax2.set_xlabel("Epoch")
ax2.grid(True)
ax2.legend()  # Add legend

# Adjust layout to prevent overlap
fig.tight_layout()

# --- Save the plot ---
figs_dir = os.path.join(os.path.dirname(__file__), "figs")
os.makedirs(figs_dir, exist_ok=True)
save_path = os.path.join(figs_dir, "training_fig.png")

plt.savefig(save_path)
print(f"Graphs generated successfully and saved to {save_path}")
