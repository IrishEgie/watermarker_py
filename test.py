import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Create figure
fig = plt.figure(figsize=(10, 8))

# Create GridSpec with custom layout (3 rows, 3 columns)
gs = gridspec.GridSpec(nrows=3, ncols=3, figure=fig)

# Define subplots within the GridSpec
ax1 = fig.add_subplot(gs[0, 0])  # First row, first column
ax2 = fig.add_subplot(gs[0, 1:])  # First row, spanning second and third columns
ax3 = fig.add_subplot(gs[1:, 0])  # Second and third rows, first column
ax4 = fig.add_subplot(gs[1:, 1:])  # Bottom-right section

# Plot data
ax1.plot([1, 2, 3], [1, 4, 9])
ax2.plot([1, 2, 3], [9, 4, 1])
ax3.plot([1, 2, 3], [3, 6, 9])
ax4.plot([1, 2, 3], [1, 2, 3])

# Set titles for each subplot
ax1.set_title("Subplot 1")
ax2.set_title("Subplot 2")
ax3.set_title("Subplot 3")
ax4.set_title("Subplot 4")

# Adjust layout to prevent overlap
plt.tight_layout()

# Show plot
plt.show()
