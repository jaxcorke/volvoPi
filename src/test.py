import subprocess

output = subprocess.check_output("iwctl station wlan0 show")
decoded_output = output.decode("utf-8")
print(decoded_output)


