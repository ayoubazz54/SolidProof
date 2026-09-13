import subprocess
import sys

lean_file = sys.argv[1]

result = subprocess.run(
    ["lake", "env", "lean", lean_file],
    capture_output = True,
    text = True
)

if result.returncode == 0:
    print("VERIFIED")
else:
    print("FAILED")
    print(result.stdout)
    print(result.stderr)
