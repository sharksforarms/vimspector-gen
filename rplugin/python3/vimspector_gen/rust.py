import subprocess
import json
import re
import argparse

# Returns an array
# [[target_name, target_file, target_args]]
def _get_targets_from_cargo():
    CARGO_CMD = [
        "cargo",
        "build",
        "--workspace",
        "--all-targets",
        "--message-format=json"
    ]

    cargo_out_json = subprocess.check_output(CARGO_CMD, shell=False).strip()

    targets = []

    for line in cargo_out_json.splitlines():
        data = json.loads(line)

        if 'target' in data:
            target = data['target']

            if 'test' in target['kind'] \
                or 'example' in target['kind'] \
                or 'bench' in target['kind'] \
                or 'bin' in target['kind']:

                target_file = data.get('executable', None)
                if target_file is not None:
                    target_kind = ''.join(target['kind'])
                    target_name = f"{target_kind.title()} - {target['name']}"
                    target_args = []

                    if 'test' in target['kind'] and target_file is not None:
                        test_list_raw = subprocess.check_output([target_file, '--list'], shell=False).strip()
                        test_list = re.findall(rb"(.*?): test\n", test_list_raw)

                        for test in test_list:
                            test_target_name = f"{target_name} - {test.decode()}"
                            target_args = ["--exact", test.decode()]
                            targets.append([test_target_name, target_file, target_args])
                    else:
                        targets.append([target_name, target_file, target_args])

    return targets

def get_rust_configurations():
    configurations = {}

    for target in _get_targets_from_cargo():
        target_name, target_file, target_args = target
        configurations[target_name] = {
            "adapter": "CodeLLDB",
            "configuration": {
                "request": "launch",
                "program": target_file,
                "args": target_args
            }
        }

    return configurations

