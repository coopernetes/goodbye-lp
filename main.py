import subprocess
import sys
import re
import json
import os
from typing import List


def get_entry(id: str):
    print(f"Getting {id}")
    return subprocess.run(["lpass", "show", "-j", id], capture_output=True)


def get_entries(ids: List[str]):
    results = [ get_entry(id) for id in ids ]
    successful_entries = [ json.loads(p.stdout)[0] for p in results if p.returncode == 0 ]
    failed = [ p for p in results if p.returncode != 0]
    if failed:
        print("Warning: Some entries failed to be fetched")
        for p in failed:
            print(f"Out: {p.stdout}, err: {p.stderr}")
    return successful_entries


def main():
    p = subprocess.run(["lpass", "status"], capture_output=True)
    if p.returncode != 0:
        print(f"Error encountered (are you logged in?), output: {p.stdout} err: {p.stderr}")
        return p.returncode
    ls = subprocess.run(["lpass", "ls"], capture_output=True)
    if ls.returncode != 0:
        print(f"Error encountered while listing entries, output: {ls.stdout} err: {ls.stderr}")
        return p.returncode
    
    split = ls.stdout.decode("utf-8").split("\n")
    entries = [ s for s in split if s != "" ]
    print(f"Found {len(entries)} entries")
    ids = []
    for e in entries:
        match = re.match(r'^.+\[id: (\d+)\]$', e)
        if match and len(match.groups()) == 1:
            ids.append(match.group(1))
        else:
            print(f"Could not match on id for line {e}")

    output_json = get_entries(ids)
    out_dir = os.path.join(os.curdir, "out")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    output_file = os.path.join(out_dir, f"lastpass.json")
    with open(output_file, 'w') as f:
        f.write(json.dumps(output_json))
    return 0


if __name__ == '__main__':
    sys.exit(main())
