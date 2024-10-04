#!/bin/python3

import os
import sys
import json
import signal
import subprocess as sp

progs = []  
terminated = False  
spsignal = signal.SIGTERM  

def handle_signal(*args):
    global terminated
    terminated = True
    for prog in progs:
        prog.send_signal(spsignal)

def parse_args():
    return list(map(lambda x: x.strip().split(), ' '.join(sys.argv[1:]).split('|')))

def setup_signal_handler():
    signal.signal(signal.SIGUSR1, handle_signal)

def run_processes(args):
    global progs

    file_input = None

    for i, cmd in enumerate(args):
        spstdin = None
        if len(cmd) > 2 and cmd[-2] == '<':
            file_input = open(cmd[-1], 'r')
            cmd = cmd[:-2]
            spstdin = file_input

        if i == 0:
            spstdin = spstdin if spstdin else sys.stdin
        else:
            spstdin = spstdin if spstdin else progs[i - 1].stdout

        progs.append(sp.Popen(cmd, stdin=spstdin, stdout=sp.PIPE, text=True))

    return progs

def collect_results(progs, args):
    global terminated
    results = []

    for i, prog in enumerate(progs):
        exit_code = prog.wait()

        result = {
            'name': args[i][0],
            'code': exit_code if not terminated else -spsignal
        }

        if terminated:
            result['signal'] = 'Terminated'

        if i == len(progs) - 1:
            result['output'] = prog.stdout.read()

        results.append(result)

    return results

def write_results_to_file(results, filename='ioutput.json'):
    with open(filename, 'w', encoding='utf8', newline='\n') as f:
        f.write(json.dumps(results, indent=2))

def print_results(results):
    print(json.dumps(results, indent=2))

def main():
    print('current PID:', os.getpid())
    setup_signal_handler()
    args = parse_args()
    progs = run_processes(args)
    results = collect_results(progs, args)
    write_results_to_file(results)
    print_results(results)

if __name__ == "__main__":
    main()
