import subprocess


def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(f"[<] Shell command output: {result.stdout}")
        if result.stderr:
            print(f"[x] Shell command error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"[x] Error running shell command: {e}")
        return False