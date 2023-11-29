import sys

import pandas as pd
from CalculateMomentInertia import MomentInertiaDisc
import matplotlib.pyplot as plt


def create_data(data):
    """
    :param data: {"dist_center_segment": d_list, "radius_segment": r_list,
                'center_mass': center_mass_list, "jx_y": jx_y, "jz_y": jz_y, "jz_x": jz_x}
    :return:None
    """
    data = pd.DataFrame(data)
    data.to_csv('Data/output.csv', encoding='utf-8')


def plot_graf(data):
    """
    :param data: {"dist_center_segment": d_list, "radius_segment": r_list,
                'center_mass': center_mass_list, "jx_y": jx_y, "jz_y": jz_y, "jz_x": jz_x}
    :return:
    """
    x = data["dist_center_segment"]
    y = data["radius_segment"]
    z1 = data["center_mass"]
    z2 = data["jx_y"]

    # Transform it to a long format
    ax = plt.figure(3).add_subplot(projection='3d')
    plt.xlabel("\n Растояние между \n центрами диска и отверстия (м)")
    plt.ylabel("\n Радиус отверстия (м)")
    plt.title("Поиск зависимостей смещения центра масс")
    ax.plot_trisurf(x, y, z1, linewidth=0.3, antialiased=True)
    ax = plt.figure(4).add_subplot(projection='3d')
    plt.xlabel("\n Растояние между \n центрами диска и отверстия (м)")
    plt.ylabel("\n Радиус отверстия (м)")
    plt.title("jx_y")
    ax.plot_trisurf(x, y, z2, linewidth=0.3, antialiased=True)
    plt.show()


def main(script_user_do=False):

    jx_y, jz_x, jz_y, center_mass_list = [], [], [], []

    if script_user_do:
        values = {"thickness": 0, "radius_segment": 0,
                  "radius_disc": 0, "dist_center_segment": 0, "material_density": 0}
        try:
            for i in values.keys():
                values[i] = float(input(f"Enter {i}: "))
        except TypeError:
            print("Не тот тип данных")
            sys.exit()
        except ValueError:
            print('Что-то пошло не так')
            sys.exit()
    else:
        values = {"thickness": 0.04, "radius_segment": 0.035,
                  "radius_disc": 0.1, "dist_center_segment": 0.03, "material_density": 250}

    new_disc = MomentInertiaDisc(values["thickness"],
                                 values["radius_segment"],
                                 values["radius_disc"],
                                 values["dist_center_segment"],
                                 values["material_density"])

    d_list, r_list = [], []
    for d in range(0, 96):
        r_max = int((values["radius_disc"] - d/1000)*1000)
        for r in range(0, r_max):
            new_disc.set_dist_center_segment(d/1000)
            new_disc.set_radius_segment(r/1000)
            tensor = new_disc.get_tensor_inertia()
            center_mass_list.append(new_disc.get_center_mass())
            jx_y.append(tensor[0, 0] / tensor[1, 1])
            jz_y.append(tensor[2, 2] / tensor[1, 1])
            jz_x.append(tensor[2, 2] / tensor[0, 0])
            d_list.append(d/1000)
            r_list.append(r/1000)

    for_plot = {"dist_center_segment": d_list, "radius_segment": r_list,
                'center_mass': center_mass_list, "jx_y": jx_y, "jz_y": jz_y, "jz_x": jz_x}
    create_data(for_plot)
    plot_graf(for_plot)


if __name__ == "__main__":
    # Если хотите задать свои начальные параметры: main(True)
    main()
