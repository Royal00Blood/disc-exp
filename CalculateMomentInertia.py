import numpy as np


class MomentInertiaDisc:

    def __init__(self, thickness, radius_segment, radius_disc, dist_center_segment, material_density):
        """
        :param thickness: Толщина диска.
        :param radius_segment: Радиус сегмента-отверстия.
        :param radius_disc: радиус диска.
        :param dist_center_segment: Растояние от центра диска до центра отверстия.
        :param material_density: Плотность материала диска.
        """
        self.__h = thickness
        self.__r = radius_segment
        self.__R = radius_disc
        self.__d = dist_center_segment
        self.__mr = -material_density * np.pi * self.__r**2 * self.__h
        self.__mh =  material_density * np.pi * self.__R**2 * self.__h
        self.__tensor_inert = None
        self.__c = 0

    def __calculate_tensor_inertia(self):
        self.__c = self.get_center_mass()
        jx = self.__calculate_movement_inert_x()
        jy = self.__calculate_movement_inert_y()
        jz = self.__calculate_movement_inert_z()
        self.__tensor_inert = np.array([[jx, 0, 0], [0, jy, 0], [0, 0, jz]], float)

    def __calculate_movement_inert_x(self):
        jx_sigment = 1 / 12 * self.__mr * (self.__h**2 + 3 * self.__r**2)
        jx_disc    = 1 / 12 * self.__mh * (self.__h**2 + 3 * self.__R**2)
        return jx_disc + jx_sigment

    def __calculate_movement_inert_y(self):
        jy_sigment = 1 / 12 * self.__mr * (self.__h**2 + 3 * self.__r**2) + self.__mr * self.__d**2 + \
                     self.__mr * self.__c**2
        jy_disc    = 1 / 12 * self.__mh * (self.__h**2 + 3 * self.__R**2) + self.__mh * self.__c**2
        return jy_disc + jy_sigment

    def __calculate_movement_inert_z(self):
        jz_sigment = 6 / 12 * self.__mr * self.__r**2 + self.__mr * self.__d**2 + self.__mr * self.__c**2
        jz_disc    = 6 / 12 * self.__mh * self.__R**2 + self.__mh * self.__R**2 + self.__mh * self.__c**2
        return jz_disc + jz_sigment

    def get_tensor_inertia(self):
        """
        :return: Matrix 3 х 3 - tensor inertion (состоит из осевых моментов инерции: Jx[0,0], Jy[1,1], Jz[2,2])
        """
        self.__calculate_tensor_inertia()
        return self.__tensor_inert

    def set_dist_center_segment(self, dist_center_segment):
        """
        :param dist_center_segment: Растояние от центра диска до центра отверстия.
        :return: None
        """
        self.__d = dist_center_segment

    def set_radius_segment(self, radius_segment):
        """
        :param radius_segment: Радиус сегмента-отверстия.
        :return: None
        """
        self.__r = radius_segment

    def get_center_mass(self):
        return (self.__d * self.__r**2) / (self.__R**2 - self.__r**2)
