import os.path
import pathlib
from dataclasses import dataclass
from typing import Union


@dataclass
class Cli:
    pacs_imaging_input_path: Union[str, pathlib.Path]
    ris_rad_opinion_input_path: Union[str, pathlib.Path]
    lims_pathology_input_path: Union[str, pathlib.Path]

    def validate(self):
        at_least_one_input_is_given=True

        ipath = self.pacs_imaging_input_path
        if not (os.path.isdir(ipath) or os.path.isfile(ipath)):
            raise FileNotFoundError(f'Take care, given input path does not exist for "PACS": "{ipath}"!')
        ipath = self.ris_rad_opinion_input_path
        if not (os.path.isdir(ipath) or os.path.isfile(ipath)):
            raise FileNotFoundError(f'Take care, given input path does not exist for "RIS": "{ipath}"!')
        ipath = self.lims_pathology_input_path
        if not (os.path.isdir(ipath) or os.path.isfile(ipath)):
            raise FileNotFoundError(f'Take care, given input path does not exist for "LISM": "{ipath}"!')
