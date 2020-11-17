import subprocess
import json
import re
import argparse
import os

# Returns an array
# [[target_name, target_file, target_args]]
def _get_targets_from_cargo():
    targets = []
    errors = []

    CARGO_CMD = [
        "cargo",
        "build",
        "--workspace",
        "--all-targets",
        "--message-format=json"
    ]

    cargo_proc = subprocess.run(CARGO_CMD, shell=False, capture_output=True)

    cargo_out_json = cargo_proc.stdout.strip()

    if cargo_proc.returncode != 0:
        errors.append(cargo_proc.stderr)

    for line in cargo_out_json.splitlines():
        data = json.loads(line)

        if 'target' in data:
            target = data['target']
            profile = data['profile']

            target_file = data.get('executable', None)
            if 'test' in target['kind'] \
                or 'example' in target['kind'] \
                or 'bench' in target['kind'] \
                or 'bin' in target['kind']:

                if target_file is not None:
                    target_kind = ''.join(target['kind'])
                    target_name = f"{target_kind.title()} - {target['name']}"
                    target_args = []

                    # if a test, make each test a target
                    if  profile['test'] and target_file is not None:
                        target_dir = os.path.dirname(target_file)
                        test_list_raw = subprocess.check_output([target_file, '--list'], \
                                shell=False, cwd=target_dir).strip()
                        test_list = re.findall(rb"(.*?): test\n", test_list_raw)

                        for test in test_list:
                            test_target_name = f"{target_name} - {test.decode()}"
                            target_args = ["--exact", test.decode()]
                            targets.append([test_target_name, target_file, target_args])
                    else:
                        targets.append([target_name, target_file, target_args])

    return targets, errors

def get_rust_configurations():
    configurations = {}

    targets, errors = _get_targets_from_cargo()
    for target in targets:
        target_name, target_file, target_args = target
        configurations[target_name] = {
            "adapter": "CodeLLDB",
            "configuration": {
                "request": "launch",
                "program": target_file,
                "args": target_args
            }
        }

    return configurations, errors

