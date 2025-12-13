import sys
import subprocess
import tempfile

FORBIDDEN = ['os', 'sys', 'subprocess', 'shutil']

def main():
    code = sys.stdin.read()

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
            input=None,
            capture_output=True,
            text=True,
            timeout=2
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

    except subprocess.TimeoutExpired:
        print("Time limit exceeded", file=sys.stderr)

if __name__ == '__main__':
    main()
