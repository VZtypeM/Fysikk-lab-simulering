import matplotlib.pyplot as plt


def plt_function(x, y_list, title: str, ylabel: str, save_name="figure", save_format=""):
    figure = plt.figure(title, figsize=(8, 4))

    if type(y_list) == list:
        for y in y_list:
            plt.plot(x, y)
    else:
        plt.plot(x, y_list)

    plt.title(title)
    plt.xlabel('$x$ (mm)')
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()

    if save_format == "pdf":
        figure.savefig(f"{save_name}.pdf", bbox_inches='tight')
    if save_format == "png":
        figure.savefig(f"{save_name}.png", bbox_inches='tight')
