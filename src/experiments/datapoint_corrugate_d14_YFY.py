import matplotlib.pyplot as plt

# Define the data
blank_size_sb = [1802 * 650, 1785 * 718, 1445 * 1164, 1032 * 856]
blank_size_ac = [788 * 777, 788 * 777, 788 * 761, 544 * 370]
blank_size_kb = [0, 0, 572 * 409, 477 * 366]

price_flat_sb = [1.69, 2.58, 2.31, 1.2615]
price_flat_ac = [0.727, 0.753, 0.868, 0.264]
price_flat_kb = [0, 0, 0.316, 0.23]

price_fold_sb = [2.5, 3.37, 3.193, 1.49]
price_fold_ac = [0.913, 0.917, 1.005, 0.559]
price_fold_kb = [0, 0, 0.316, 0]

tool_sb = [1668, 2138, 1870, 1700]
tool_ac = [2338, 1670, 715, 1100]
tool_kb = [0, 0, 605, 1100]

volume = [1600, 280, 70, 1900]

labels = ["SFF", "MT", "CFF", "MFF"]


def plot_price_flat_vs_blank_size(include_tooling=True, cal_flat=True):
    if cal_flat:
        data_list_sb = [
            (
                blank_size_sb[i],
                price_flat_sb[i] + (tool_sb[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(4)
            if price_flat_sb[i] > 0 and blank_size_sb[i] > 0
        ]
        data_list_ac = [
            (
                blank_size_ac[i],
                price_flat_ac[i] + (tool_ac[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(4)
            if price_flat_ac[i] > 0 and blank_size_ac[i] > 0
        ]
        data_list_kb = [
            (
                blank_size_kb[i],
                price_flat_kb[i] + (tool_kb[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(4)
            if price_flat_kb[i] > 0 and blank_size_kb[i] > 0
        ]
    else:
        data_list_sb = [
            (
                blank_size_sb[i],
                price_fold_sb[i] + (tool_sb[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(4)
            if price_fold_sb[i] > 0 and blank_size_sb[i] > 0
        ]
        data_list_ac = [
            (
                blank_size_ac[i],
                price_fold_ac[i] + (tool_ac[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(4)
            if price_fold_ac[i] > 0 and blank_size_ac[i] > 0
        ]
        data_list_kb = [
            (
                blank_size_kb[i],
                price_fold_kb[i] + (tool_kb[i] / volume[i] if include_tooling else 0),
                labels[i],
            )
            for i in range(4)
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
        "YFY d14 Price vs. Blank Size (flat)"
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
    plot_price_flat_vs_blank_size(include_tooling=True, cal_flat=True)
    plot_price_flat_vs_blank_size(include_tooling=True, cal_flat=False)
    plot_price_flat_vs_blank_size(include_tooling=False, cal_flat=True)
    plot_price_flat_vs_blank_size(include_tooling=False, cal_flat=False)
