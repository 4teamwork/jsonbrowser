import errno
import json
import os


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def dump_pretty_json(data, stream):
    json.dump(
        data, stream,
        sort_keys=True,
        indent=4,
        separators=(',', ': '))
