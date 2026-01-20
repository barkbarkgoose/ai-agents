# run with `python tmux_test.py && tmux attach -t hello_test`
import subprocess

subprocess.run([
    "tmux",
    "new-session",
    "-d",
    "-s", "hello_test",
    "echo 'hello there'; sleep 5"
])