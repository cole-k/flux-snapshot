#!/usr/bin/env python3
import argparse
import pathlib
import subprocess
import os
import sys
import re
from datetime import datetime

def make_filename(exit_code):
    '''
    Makes a filename from the current timestamp and flux's exit_code.
    '''
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    return f'{timestamp}-exit{exit_code}'

def get_output_dir(directory):
    '''
    Gets a path to the output directory, creating it if it doesn't exist.
    '''
    output_dir = pathlib.Path(directory or '.', 'flux-snapshot')
    output_dir.mkdir(exist_ok=True)
    return output_dir

def run_flux_command(command, args, directory):
    '''
    Runs the flux command in the given directory, capturing its output in
    color.

    This works because cargo and rustc both take a --color option.
    '''
    return subprocess.run([command, '--color', 'always'] + args, cwd=directory,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def run_git_command(args, directory):
    return subprocess.run(['git'] + args, cwd=directory, check=True)

def strip_ansi_escape_codes(text):
    '''
    https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python/38662876#38662876

    Strips ANSI escape codes (color codes) from the output.
    '''
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def save_flux_output(flux_output, directory):
    filename = make_filename(flux_output.returncode)
    output_dir = get_output_dir(directory)
    file_contents = strip_ansi_escape_codes(flux_output.stdout.decode('utf-8'))
    with open(output_dir.joinpath(filename), 'x') as f:
        f.write(file_contents)

def main():
    arg_parser = argparse.ArgumentParser(
        prog='flux-history',
        description='Run flux and save its output and a snapshot of the current repo as a git commit'
        )
    arg_parser.add_argument('flux_args', nargs='*', metavar='ARG', help='args for flux')
    arg_parser.add_argument('-d', '--dir', metavar='DIR', type=pathlib.Path,
                            dest='directory', help='directory to run flux-history in')
    arg_parser.add_argument('-m', '--message', metavar='M', default='flux-snapshot auto commit (no message)',
                            dest='commit_message', help='message for the snapshot (passed to the git commit)')
    arg_parser.add_argument('--rustc', dest='run_rustc', action='store_true',
                            help='run rustc-flux instead of cargo-flux')
    args = arg_parser.parse_args()

    flux_output = run_flux_command('rustc-flux' if args.run_rustc else 'cargo-flux',
                                   args.flux_args, args.directory)

    sys.stdout.buffer.write(flux_output.stdout)

    save_flux_output(flux_output, args.directory)

    run_git_command(['add', '.'], args.directory)

    run_git_command(['commit', '-m', args.commit_message], args.directory)

if __name__ == '__main__':
    main()
