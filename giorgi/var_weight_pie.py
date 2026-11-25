import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

# Hierarchical structure from the spreadsheet:
# Policy Objective -> Groups -> (Variable name, Final weight)
hierarchy = [
    {
        "objective": "Ecosystem Vitality",
        "obj_color": "#81D41A",
        "groups": [
            {
                "group": "Ecosystem Services",
                "grp_color": "#BBE33D",
                "var_color": "#E6F4B8",
                "vars": [
                    ("Tree cover loss", 0.102719359620898),
                    ("Grassland loss", 0.0171198932701496),
                    ("Wetland loss", 0.0171198932701496),
                ],
            },
            {
                "group": "Agriculture",
                "grp_color": "#A3D936",
                "var_color": "#ECF7C8",
                "vars": [
                    ("Sustainable Pesticide Use", 0.0542264301946445),
                    ("Sustainable Nitrogen Management Index", 0.0542264301946445),
                ],
            },
            {
                "group": "Water Resources",
                "grp_color": "#8BC92E",
                "var_color": "#F2FAD8",
                "vars": [
                    ("Wastewater treatment", 0.0862658934807329),
                ],
            },
        ],
    },
    {
        "objective": "Environmental Health",
        "obj_color": "#2A6099",
        "groups": [
            {
                "group": "Air Quality",
                "grp_color": "#5983B0",
                "var_color": "#B8CCE0",
                "vars": [
                    ("PM2.5 exposure", 0.0836057365640669),
                    ("Household solid fuels", 0.0675283905651803),
                    ("Ozone exposure", 0.00803867299944329),
                    ("NOx exposure", 0.00803867299944329),
                    ("SO2 exposure", 0.00321900656963406),
                    ("CO exposure", 0.00321900656963406),
                    ("VOC exposure", 0.00321900656963406),
                ],
            },
            {
                "group": "Sanitation & Drinking Water",
                "grp_color": "#4874A3",
                "var_color": "#C5D6E8",
                "vars": [
                    ("Unsafe sanitation", 0.0448325596155492),
                    ("Unsafe drinking water", 0.0672488394233238),
                ],
            },
            {
                "group": "Heavy Metals",
                "grp_color": "#3A6696",
                "var_color": "#D2E0EE",
                "vars": [
                    ("Lead exposure", 0.0941228722760937),
                ],
            },
            {
                "group": "Waste Management",
                "grp_color": "#6B92BD",
                "var_color": "#DEE6EF",
                "vars": [
                    ("Controlled solid waste", 0.0374303301813525),
                    ("Ocean Plastics", 0.0374303301813525),
                ],
            },
        ],
    },
    {
        "objective": "Climate Change Policy Objective",
        "obj_color": "#FFBF00",
        "groups": [
            {
                "group": "Climate Change",
                "grp_color": "#FFD428",
                "var_color": "#FFF5CE",
                "vars": [
                    ("Adjusted emissions growth rate for carbon dioxide", 0.0764068552646557),
                    ("Adjusted emissions growth rate for methane", 0.0182701525764317),
                    ("Adjusted emissions growth rate for F-gases", 0.00775071880372805),
                    ("Adjusted emissions growth rate for nitrous oxide", 0.00387535940186402),
                    ("Adjusted emissions growth rate for black carbon", 0.00553637799457393),
                    ("Growth rate in carbon dioxide emissions from land cover", 0.00830404102017226),
                    ("Greenhouse gas intensity growth rate", 0.084710896284828),
                    ("Greenhouse gas emissions per capita", 0.00553637799457393),
                ],
            },
        ],
    },
]

# Flatten data across all 3 levels using Final weights
total_weight = sum(
    val for obj in hierarchy for grp in obj["groups"] for _, val in grp["vars"]
)

obj_angles, obj_starts, obj_colors, obj_labels = [], [], [], []
grp_angles, grp_starts, grp_colors, grp_labels = [], [], [], []
var_angles, var_starts, var_colors, var_labels = [], [], [], []

cursor = 0.0
for obj in hierarchy:
    obj_start = cursor
    obj_total = 0.0
    for grp in obj["groups"]:
        grp_start = cursor
        grp_total = 0.0
        for var_name, var_val in grp["vars"]:
            angle = (var_val / total_weight) * 2 * np.pi
            var_starts.append(cursor)
            var_angles.append(angle)
            var_colors.append(grp["var_color"])
            var_labels.append(f"{var_name} ({var_val * 100:.1f}%)")
            cursor += angle
            grp_total += var_val
        grp_starts.append(grp_start)
        grp_angles.append((grp_total / total_weight) * 2 * np.pi)
        grp_colors.append(grp["grp_color"])
        grp_labels.append(f"{grp['group']} ({grp_total * 100:.1f}%)")
        obj_total += grp_total
    obj_starts.append(obj_start)
    obj_angles.append((obj_total / total_weight) * 2 * np.pi)
    obj_colors.append(obj["obj_color"])
    obj_labels.append(f"{obj['objective']} ({obj_total * 100:.1f}%)")

fig, ax = plt.subplots(figsize=(11, 8), subplot_kw=dict(projection="polar"))

# Ring radii (bottom and radial thickness)
inner_bottom, inner_height = 0.25, 0.25
mid_bottom, mid_height = 0.50, 0.25
outer_bottom, outer_height = 0.75, 0.25

# 1. Inner ring: Policy Objectives
ax.bar(
    x=obj_starts,
    width=obj_angles,
    bottom=inner_bottom,
    height=inner_height,
    color=obj_colors,
    edgecolor="w",
    linewidth=1.2,
    align="edge",
)

# 2. Middle ring: Groups
ax.bar(
    x=grp_starts,
    width=grp_angles,
    bottom=mid_bottom,
    height=mid_height,
    color=grp_colors,
    edgecolor="w",
    linewidth=1.0,
    align="edge",
)

# 3. Outer ring: Variables
ax.bar(
    x=var_starts,
    width=var_angles,
    bottom=outer_bottom,
    height=outer_height,
    color=var_colors,
    edgecolor="w",
    linewidth=0.8,
    align="edge",
)

# Add labels inside larger slices
for start, width, label in zip(obj_starts, obj_angles, obj_labels):
    if width > 0.35:
        mid_angle = start + width / 2
        short_name = label.split(" (")[0].split()[0]
        ax.text(
            mid_angle,
            inner_bottom + inner_height / 2,
            short_name,
            ha="center",
            va="center",
            fontsize=8,
            fontweight="bold",
            color="#111111",
        )

for start, width, label in zip(grp_starts, grp_angles, grp_labels):
    if width > 0.45:
        mid_angle = start + width / 2
        pct = label.split("(")[-1].rstrip(")")
        ax.text(
            mid_angle,
            mid_bottom + mid_height / 2,
            pct,
            ha="center",
            va="center",
            fontsize=7.5,
            color="#111111",
        )

ax.set_ylim(0, 1.05)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_axis_off()
ax.set_title("EPI Performance Indicator Weights (Nested Hierarchy)", pad=20, fontsize=13)

plt.tight_layout()
plt.show()

