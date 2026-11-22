import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))

# Inner and middle stripe size
size = 0.3

# New method: suppress indicators with no effect on humans and allocate
# their weight within the same subgroup of indicators
# Kept indicators: Cf the spreadsheet
vals = np.array([[45.793, 0.1], [33.168, 40.], [21.039, 10.]]) # FIXME: these values have no meaning yet

# Normalize vals to 2 pi
valsnorm = vals/np.sum(vals)*2*np.pi

# Obtain the coordinates of the bar edges
valsleft = np.cumsum(np.append(0, valsnorm.flatten()[:-1])).reshape(vals.shape)

# Stripe colors
cmap = plt.colormaps["tab20c"]  # Cf tab20c.png for the colormap
outer_colors = cmap([2, 6, 10]) # Least saturated
inner_colors = cmap([1, 5, 9])  # Most saturated

# Outer stripe
ax.bar(x=valsleft[:, 0],
       width=valsnorm.sum(axis=1), bottom=1-size, height=size,
       color=outer_colors, edgecolor='w', linewidth=1, align="edge")

# Middle stripe
ax.bar(x=valsleft.flatten(),
       width=valsnorm.flatten(), bottom=1-2*size, height=size,
       color=inner_colors, edgecolor='w', linewidth=1, align="edge")

# Title
ax.set(title="EPI performance indicator weights")

# Show plots
ax.set_axis_off()
plt.show()
