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


    before_len = len(config['configurations'])
    config['configurations'].update(configurations)
    after_len = len(config['configurations'])

    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)

    return after_len - before_len

def vimspector_new_json(filename, configurations):
    config = {
        "$schema": "https://puremourning.github.io/vimspector/schema/vimspector.schema.json",
        "configurations": configurations
    }

    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)

def nvim_error(nvim, msg):
    if isinstance(msg, bytes):
        msg = msg.decode()
    nvim.err_write(f"vimspector-gen error: {msg.strip()}\n")

def nvim_info(nvim, msg):
    if isinstance(msg, bytes):
        msg = msg.decode()
    nvim.out_write(f"vimspector-gen: {msg.strip()}\n")

@pynvim.plugin
class VimspectorGen(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command('VimspectorGenerateNew', nargs='*', range='')
    def generate_new(self, args, range):
        configurations = {}
        for arg in args:
            confs, errors = GENERATOR_MAP[arg]()
            configurations.update(confs)

            for err in errors:
                nvim_error(self.nvim, err)

        vimspector_new_json(DEFAULT_FILENAME, configurations)
        nvim_info(self.nvim, f"Generated {len(configurations)} configurations!")


    @pynvim.command('VimspectorGenerateUpdate', nargs='*', range='')
    def generate_update(self, args, range):
        configurations = {}
        for arg in args:
            confs, errors = GENERATOR_MAP[arg]()
            configurations.update(confs)

            for err in errors:
                nvim_error(self.nvim, err)

        diff_len = vimspector_update_json(DEFAULT_FILENAME, configurations)
        nvim_info(self.nvim, f"Finished updating! Added {diff_len} configurations")

