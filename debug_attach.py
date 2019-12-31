'''
A simple script to aid in quickly attaching a debugger to the correct process (without needing a pid)
Charles Machalow - MIT License
'''
import argparse
import psutil
import subprocess
import re

def debugPid(pid):
    ''' attempts to start the debugger with the given pid '''
    return subprocess.call(f'powershell Debug-Process -Id {pid}', shell=True)

def getProcessViaRegexes(exe, exeArgs):
    ''' attempts to find the process matching a regex for the exe and the args to the exe '''
    for process in psutil.process_iter():
        try:
            if re.findall(exe, process.exe()):
                args = ' '.join(process.cmdline())
                if re.findall(exeArgs, args):
                    return process
        except psutil.AccessDenied:
            pass

def debugProcessViaRegexes(exe, exeArgs):
    ''' calls getProcessViaRegexes(..) the attempts to debug that process '''
    process = getProcessViaRegexes(exe, exeArgs)
    if not process:
        raise RuntimeError("Process wan't available!")

    print (f"About to attempt to attach to Process:\nPID: {process.pid}\nExe: {process.exe()}\nArgs: {' '.join(process.cmdline()[1:])}")
    debugPid(process.pid)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", '--exe', help='Regex of running executable to debug/attach to', required=True)
    parser.add_argument("-a", '--args', help='Regex of args passed to the executable to attach/debug', required=True)
    args = parser.parse_args()
    debugProcessViaRegexes(args.exe, args.args)