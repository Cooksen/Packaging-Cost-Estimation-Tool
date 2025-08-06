import matplotlib.pyplot as plt

# Define the data
# mff sff
blank_size_sb = [1032 * 856, 1802 * 650]
blank_size_ac = [544 * 370, 788 * 777]
blank_size_kb = [477 * 366, 0]

price_flat_sb = [0.993, 1.269]
price_flat_ac = [0.284, 0.682]
price_flat_kb = [0.242, 0]

price_fold_sb = [1.475, 1.844]
price_fold_ac = [0.528, 1.071]
price_fold_kb = [0, 0]

tool_sb = [0, 0]
tool_ac = [0, 0]
tool_kb = [0, 0]

volume = [0, 0]

labels = ["MFF", "SFF"]


def plot_price_flat_vs_blank_size(include_tooling=True, cal_flat=True):
    if cal_flat:
        data_list_sb = [
            (
                blank_size_sb[i],
                price_flat_sb[i] + (tool_sb[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(len(blank_size_sb))
            if price_flat_sb[i] > 0 and blank_size_sb[i] > 0
        ]
        data_list_ac = [
            (
                blank_size_ac[i],
                price_flat_ac[i] + (tool_ac[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(len(blank_size_ac))
            if price_flat_ac[i] > 0 and blank_size_ac[i] > 0
        ]
        data_list_kb = [
            (
                blank_size_kb[i],
                price_flat_kb[i] + (tool_kb[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(len(blank_size_kb))
            if price_flat_kb[i] > 0 and blank_size_kb[i] > 0
        ]
    else:
        data_list_sb = [
            (
                blank_size_sb[i],
                price_fold_sb[i] + (tool_sb[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(len(blank_size_sb))
            if price_fold_sb[i] > 0 and blank_size_sb[i] > 0
        ]
        data_list_ac = [
            (
                blank_size_ac[i],
                price_fold_ac[i] + (tool_ac[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(len(blank_size_ac))
            if price_fold_ac[i] > 0 and blank_size_ac[i] > 0
        ]
        data_list_kb = [
            (
                blank_size_kb[i],
                price_fold_kb[i] + (tool_kb[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(len(blank_size_kb))
            if price_fold_kb[i] > 0 and blank_size_kb[i] > 0
        ]

    plt.figure(figsize=(10, 6))

    if data_list_sb:
        x_sb, y_sb, label_sb = zip(*data_list_sb)
        plt.scatter(x_sb, y_sb, label="System Box", color="blue")
        for i in range(len(x_sb)):
            plt.text(x_sb[i], y_sb[i], label_sb[i], fontsize=9, ha="right", va="bottom")

    if data_list_ac:
        x_ac, y_ac, label_ac = zip(*data_list_ac)
        plt.scatter(x_ac, y_ac, label="Accessory Box", color="green")
        for i in range(len(x_ac)):
            plt.text(x_ac[i], y_ac[i], label_ac[i], fontsize=9, ha="right", va="bottom")

    if data_list_kb:
        x_kb, y_kb, label_kb = zip(*data_list_kb)
        plt.scatter(x_kb, y_kb, label="KB Tray", color="red")
        for i in range(len(x_kb)):
            plt.text(x_kb[i], y_kb[i], label_kb[i], fontsize=9, ha="right", va="bottom")

    plt.xlabel("Blank Size (m²)")
    ylabel = (
        "Adjusted Price (Price + Tooling/Volume)" if include_tooling else "Price Only"
    )
    plt.ylabel(ylabel)

    if not include_tooling:
        plt.ylim(0, 5)
    else:
        plt.ylim(0, 40)

    title = (
        "Sealed air d14 Price vs. Blank Size (flat)"
        if cal_flat
        else "Price vs. Blank Size (fold)"
    )
    title += " with Tooling Cost" if include_tooling else ""
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("price_flat_vs_blank_size_labeled.png")
    plt.show()


if __name__ == "__main__":
    # plot_price_flat_vs_blank_size(include_tooling=True,  cal_flat=True)
    # plot_price_flat_vs_blank_size(include_tooling=True,  cal_flat=False)
    plot_price_flat_vs_blank_size(include_tooling=False, cal_flat=True)
    plot_price_flat_vs_blank_size(include_tooling=False, cal_flat=False)


# # bfile_oop.py
# class d14Plotter:
#     def __init__(self):
#         self.blank_size_sb = [1802 * 650, 1785 * 718, 1445 * 1164, 1032 * 856]
#         self.blank_size_ac = [788 * 777, 788 * 777, 788 * 761, 544 * 370]
#         self.blank_size_kb = [0, 0, 572 * 409, 477 * 366]

#         self.price_flat_sb = [1.69, 2.58, 2.31, 1.2615]
#         self.price_flat_ac = [0.727, 0.753, 0.868, 0.264]
#         self.price_flat_kb = [0, 0, 0.316, 0.23]

#         self.price_fold_sb = [2.5, 3.37, 3.193, 1.49]
#         self.price_fold_ac = [0.913, 0.917, 1.005, 0.559]
#         self.price_fold_kb = [0, 0, 0.316, 0]

#         self.tool_sb = [1668, 2138, 1870, 1700]
#         self.tool_ac = [2338, 1670, 715, 1100]
#         self.tool_kb = [0, 0, 605, 1100]

#         self.volume = [1600, 280, 70, 1900]

#     def get_data(self, include_tooling=True, cal_flat=True):
#         data = []
#         for i in range(4):
#             if cal_flat:
#                 price_sb = self.price_flat_sb[i]
#                 price_ac = self.price_flat_ac[i]
#                 price_kb = self.price_flat_kb[i]
#             else:
#                 price_sb = self.price_fold_sb[i]
#                 price_ac = self.price_fold_ac[i]
#                 price_kb = self.price_fold_kb[i]

#             if price_sb > 0 and self.blank_size_sb[i] > 0:
#                 price = price_sb + (self.tool_sb[i] / self.volume[i] if include_tooling else 0)
#                 data.append(('SB', self.blank_size_sb[i], price))
#             if price_ac > 0 and self.blank_size_ac[i] > 0:
#                 price = price_ac + (self.tool_ac[i] / self.volume[i] if include_tooling else 0)
#                 data.append(('AC', self.blank_size_ac[i], price))
#             if price_kb > 0 and self.blank_size_kb[i] > 0:
#                 price = price_kb + (self.tool_kb[i] / self.volume[i] if include_tooling else 0)
#                 data.append(('KB', self.blank_size_kb[i], price))
#         return data
