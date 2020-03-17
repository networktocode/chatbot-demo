from subprocess import Popen, PIPE
import re

def run_command(command):
    process = Popen(
        command, stdout=PIPE, stderr=PIPE
    )
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8')

def ipcalc(subnet):
    command_output = run_command(
        ['ipcalc', '{}'.format(subnet)]
    )
    return command_output

