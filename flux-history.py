#!/usr/bin/env python3
import argparse
import pathlib
import git
import subprocess
import os
from datetime import datetime

def run_flux_command(command, args, directory):
    # Runs the command in the specified directory and pipes stderr to stdout and
    # captures stdout
    return subprocess.run([command] + args, cwd=directory,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def run_git_command(args, directory):
    return subprocess.run(['git'] + args, cwd=directory, check=True)

def save_flux_output(flux_output, directory):
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{timestamp}-exit{flux_output.returncode}'
    flux_output_dir = pathlib.Path(directory or '.', 'flux-snapshot')
    flux_output_dir.mkdir(exists_ok=True)
    with open(flux_output_dir.joinpath(filename), 'x') as f:
        f.write(flux_output.stdout)

def main():
    arg_parser = argparse.ArgumentParser(
        prog='flux-history',
        description='Run flux and save its output and a snapshot of the current repo as a git commit'
        )
    arg_parser.add_argument('flux_args')
    arg_parser.add_argument('args', nargs='*', metavar='ARG', help='args for flux')
    arg_parser.add_argument('-d', '--dir', metavar='DIR', type=pathlib.Path,
                            dest='directory', help='directory to run flux-history in')
    arg_parser.add_argument('-m', '--message', metavar='M', default='flux-snapshot auto commit (no message)',
                            dest='commit_message', help='message for the snapshot (passed to the git commit)')
    arg_parser.add_argument('--rustc', dest='run_rustc', action='store_true',
                            help='run rustc-flux instead of cargo-flux')
    args = arg_parser.parse_args()

    flux_output = run_flux_command('rustc-flux' if args.run_rustc else 'cargo-flux',
                                   arg_parser.flux_args, arg_parser.directory)
    save_flux_output(flux_output, arg_parser.directory)

    run_git_command(['add', '.'], arg_parser.directory)

    run_git_command(['commit', '-m', arg_parser.commit_message], arg_parser.directory)

if __name__ == '__main__':
    main()
