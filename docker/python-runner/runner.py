import sys
import subprocess
import tempfile

FORBIDDEN = ['os', 'sys', 'subprocess', 'shutil']
SEPARATOR = '###INPUT###'





import sys
import subprocess
import tempfile

FORBIDDEN = ['os', 'sys', 'subprocess', 'shutil']
SEPARATOR = '###INPUT###'


def main():
    data = sys.stdin.read()

    if SEPARATOR in data:
        code, user_input = data.split(SEPARATOR, 1)
        code = code.rstrip()
        user_input = user_input.lstrip()
    else:
        code = data
        user_input = ""

    for word in FORBIDDEN:
        if f"import {word}" in code:
            print(f"Forbidden import: {word}", file=sys.stderr)
            return

    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        delete=False
    ) as f:
        f.write(code)
        path = f.name

    try:
        result = subprocess.run(
            ['python', path],
            input=user_input,
            capture_output=True,
            text=True,
            timeout=2
        )
        print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, file=sys.stderr, end='')

    except subprocess.TimeoutExpired:
        print("Time limit exceeded", file=sys.stderr)


if __name__ == '__main__':
    main()