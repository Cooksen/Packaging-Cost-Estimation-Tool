import matplotlib.pyplot as plt

# Define the data
blank_size_sb = [2260 * 1022, 2507 * 891, 1334 * 1032]
blank_size_ac = [949 * 1061 + 826 * 330, 1137 * 1083 + 848 * 330]
blank_size_kb = [0]

price_flat_sb = [8.100, 10.336, 9.980]
price_flat_ac = [2.335, 2.335]
price_flat_kb = [0]

tool_sb = [1668, 2138, 1870]
tool_ac = [2338, 1670]
tool_kb = [0]

volume = [73000, 4000]

labels_sb = ["DT_base_outer_box", "DT_expansion_outer_box", "DT_expansion_outer_box_2"]
labels_ac = ["DT_base_accessory_box", "DT_expansion_accessory_box"]


def plot_price_flat_vs_blank_size(include_tooling=True, cal_flat=True):
    # Compute adjusted price and filter out entries with zero price or blank size
    data_list_sb = [
        (
            blank_size_sb[i],
            price_flat_sb[i] + (tool_sb[i] / volume[i] if include_tooling else 0),
            labels_sb[i],
        )
        for i in range(len(blank_size_sb))
        if price_flat_sb[i] > 0 and blank_size_sb[i] > 0
    ]
    data_list_ac = [
        (
            blank_size_ac[i],
            price_flat_ac[i] + (tool_ac[i] / volume[i] if include_tooling else 0),
            labels_ac[i],
        )
        for i in range(len(blank_size_ac))
        if price_flat_ac[i] > 0 and blank_size_ac[i] > 0
    ]
    data_list_kb = [
        (blank_size_kb[i], price_flat_kb[i], f"KB_{i}")
        for i in range(len(blank_size_kb))
        if price_flat_kb[i] > 0 and blank_size_kb[i] > 0
    ]

    # Plotting
    plt.figure(figsize=(10, 6))

    # Unpack and plot each dataset
    if data_list_sb:
        x_sb, y_sb, label_sb = zip(*data_list_sb)
        plt.scatter(x_sb, y_sb, label="System Box", color="blue")
        for i in range(len(x_sb)):
            plt.annotate(
                label_sb[i],
                (x_sb[i], y_sb[i]),
                textcoords="offset points",
                xytext=(5, 5),
                ha="left",
                fontsize=9,
            )

    if data_list_ac:
        x_ac, y_ac, label_ac = zip(*data_list_ac)
        plt.scatter(x_ac, y_ac, label="Accessory Box", color="green")
        for i in range(len(x_ac)):
            plt.annotate(
                label_ac[i],
                (x_ac[i], y_ac[i]),
                textcoords="offset points",
                xytext=(5, 5),
                ha="left",
                fontsize=9,
            )

    if data_list_kb:
        x_kb, y_kb, label_kb = zip(*data_list_kb)
        plt.scatter(x_kb, y_kb, label="KB Tray", color="red")
        for i in range(len(x_kb)):
            plt.annotate(
                label_kb[i],
                (x_kb[i], y_kb[i]),
                textcoords="offset points",
                xytext=(5, 5),
                ha="left",
                fontsize=9,
            )

    plt.xlabel("Blank Size (m²)")
    ylabel = (
        "Adjusted Price (Price + Tooling/Volume)" if include_tooling else "Price Only"
    )
    plt.ylabel(ylabel)

    plt.title(
        "YFY D15 Brickyard Base and Expension Price vs. Blank Size (flat)"
        + (" with Tooling Cost" if include_tooling else "")
    )
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("price_flat_vs_blank_size_labeled_offset.png")
    plt.show()


# Call the function from main
if __name__ == "__main__":
    plot_price_flat_vs_blank_size(include_tooling=False, cal_flat=True)


# afile_oop.py

# class d15Plotter:
#     def __init__(self):
#         # Define the data for afile
#         self.blank_size_sb = [2260 * 1022, 2507 * 891, 1334 * 1032]
#         self.blank_size_ac = [949 * 1061 + 826 * 330, 1137 * 1083 + 848 * 330]
#         self.blank_size_kb = [0]

#         self.price_flat_sb = [8.100, 10.336, 9.980]
#         self.price_flat_ac = [2.335, 2.335]
#         self.price_flat_kb = [0]

#         self.tool_sb = [1668, 2138, 1870]
#         self.tool_ac = [2338, 1670]
#         self.tool_kb = [0]

#         self.volume = [73000, 4000]

#     def get_data(self, include_tooling=True):
#         data_list = []

#         # SB data
#         for i in range(len(self.blank_size_sb)):
#             if self.price_flat_sb[i] > 0 and self.blank_size_sb[i] > 0:
#                 tooling_cost = self.tool_sb[i] / self.volume[i] if include_tooling and i < len(self.volume) else 0
#                 adjusted_price = round(self.price_flat_sb[i] + tooling_cost, 3)
#                 data_list.append((self.blank_size_sb[i], adjusted_price, f"SB-{i+1}"))

#         # AC data
#         for i in range(len(self.blank_size_ac)):
#             if self.price_flat_ac[i] > 0 and self.blank_size_ac[i] > 0:
#                 tooling_cost = self.tool_ac[i] / self.volume[i] if include_tooling and i < len(self.volume) else 0
#                 adjusted_price = round(self.price_flat_ac[i] + tooling_cost, 3)
#                 data_list.append((self.blank_size_ac[i], adjusted_price, f"AC-{i+1}"))

#         # KB data
#         for i in range(len(self.blank_size_kb)):
#             if self.price_flat_kb[i] > 0 and self.blank_size_kb[i] > 0:
#                 tooling_cost = self.tool_kb[i] / self.volume[i] if include_tooling and i < len(self.volume) else 0
#                 adjusted_price = round(self.price_flat_kb[i] + tooling_cost, 3)
#                 data_list.append((self.blank_size_kb[i], adjusted_price, f"KB-{i+1}"))

#         return data_list
