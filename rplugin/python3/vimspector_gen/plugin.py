import json

import pynvim

from .rust import get_rust_configurations

DEFAULT_FILENAME = ".vimspector.json"

GENERATOR_MAP = {
    'rust': get_rust_configurations,
}

def vimspector_update_json(filename, configurations):
    config = {}

    with open(filename, 'r') as f:
        config = json.load(f)

    config['configurations'].update(configurations)

    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)

def vimspector_new_json(filename, configurations):
    config = {
        "$schema": "https://puremourning.github.io/vimspector/schema/vimspector.schema.json",
        "configurations": configurations
    }

    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)

@pynvim.plugin
class VimspectorGen(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command('VimspectorGenerateNew', nargs='*', range='')
    def generate_new(self, args, range):
        configurations = {}
        for arg in args:
            confs = GENERATOR_MAP[arg]()
            configurations.update(confs)

        vimspector_new_json(DEFAULT_FILENAME, configurations)


    @pynvim.command('VimspectorGenerateUpdate', nargs='*', range='')
    def generate_update(self, args, range):
        configurations = {}
        for arg in args:
            confs = GENERATOR_MAP[arg]()
            configurations.update(confs)

        vimspector_update_json(DEFAULT_FILENAME, configurations)

