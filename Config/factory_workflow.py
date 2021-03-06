# -*- coding: utf-8 -*-
import networkx as nx
import json
import os
import pathlib
import matplotlib.pyplot as plt
import pylab
from operator import itemgetter
from statistics import mean

class Workflow(object):

    def __init__(self, workflow_file):
        super().__init__()
        self.workflow = Workflow.__load_workflow(workflow_file)

    def __str__(self):
        return self.workflow.__str__()

    def __repr__(self):
        return self.workflow.__repr__()

    def get_base_materials(self):
        return [part for part, properties in self.workflow.items() if not properties['ingredients']]

    def get_ingredients(self, part_name):
        return self.workflow[part_name]['ingredients']

    def get_base_ingredients_for_part_with_quantities(self, part_name):
        base_mats_names = self.get_base_materials()
        all_materials = self.get_ingredients(part_name)
        return {mat: quantity for mat, quantity in all_materials.items() if mat in base_mats_names}

    def get_complex_ingredients_for_part_with_quantities(self, part_name):
        base_mats_names = self.get_base_materials()
        all_materials = self.get_ingredients(part_name)
        return {mat: quantity for mat, quantity in all_materials.items() if mat not in base_mats_names}

    @staticmethod
    def __load_workflow(filename) -> dict:
        if not os.path.isfile(filename):
            print("There is no cached {0}".format(filename))
            return None

        with open(filename, 'r') as f:
            return json.load(f)

    @staticmethod
    def __dump_workflow(dictionary : dict, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps(dictionary, indent=4))