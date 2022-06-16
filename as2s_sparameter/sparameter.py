# -*- coding: utf-8 -*-

import os

import skrf as rf


class Sparameter_private:
    def __init__(self) -> None:
        pass

    def touchstone_2_network(self, path):
        return rf.Network(path)

    def network_2_dataframe(self, ntwk, attrs=['s_db'], ports=None):
        return rf.network_2_dataframe(ntwk, attrs, ports)

    def network_2_touchstone(self, ntwk, path, form):
        basename_without_ext = os.path.splitext(os.path.basename(path))[0]
        ntwk.write_touchstone(filename=basename_without_ext, dir=None, form=form)

    def network_2_spreadsheet(self, ntwk, path, form):
        ntwk.network_2_spreadsheet(ntwk, path, 'csv', form)


class Sparameter:
    def __init__(self) -> None:
        self.__p_func = Sparameter_private()

    @property
    def port(self):
        return self.__ntwk_data.number_of_ports

    def read(self, path):
        _, ext = os.path.splitext(os.path.basename(path))
        if ext == '.csv':
            self.__p_func.read_csv(path)
        else:
            self.__ntwk_data = self.__p_func.touchstone_2_network(path)

    def write(self, path, form='db', output_ext=''):
        if output_ext == 'csv':
            self.__write_csv(path, form)
        else:
            self.__p_func.write_touchstone(path, form)

    def convert(self, file_path, form='db', output_type='dataframe', output_path=None):
        # path is read as self.__ntwk_data
        self.read(file_path)
        # match output_type
        match output_type:
            case 'df':
                return self.__p_func.network_2_dataframe(self.__ntwk_data)
            case 'ts':
                self.__p_func.network_2_touchstone(self.__ntwk_data, output_path, form)
            case 'csv':
                self.__p_func.network_2_spreadsheet(self.__ntwk_data, output_path, form)
            case _:
                raise ValueError('[output_type] must be either [df],[ts],[csv]')
