import matplotlib.pyplot as plt

def plot_data(data, x_labels, title, x_text, y_text, x_point, y_point, x_off_set, y_off_set):
    plt.plot(data, 'o--', lw=1, ms=10, color='black')
    plt.xticks(range(len(data)), x_labels)
    plt.xlabel(str(x_text), fontsize=12)
    plt.ylabel(str(y_text), fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(color='grey', linestyle='-', linewidth=0.2)

    plt.axvline(x=x_point, color='r', linestyle='--')
    plt.axhline(y=y_point, color='g', linestyle='--')
    
    plt.annotate(f'{y_point:.3f}',
                 fontsize=10,
                 xy=(x_point, y_point), xycoords='data',
                 xytext=(x_off_set, y_off_set), textcoords='offset points',
                 arrowprops=dict(arrowstyle="->", lw=1, color='red'),
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1))