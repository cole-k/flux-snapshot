# flux-snapshot

`flux-snapshot` is a utility for automatically logging the output of
[`flux`](https://github.com/flux-rs/flux) (either used as `cargo-flux` or
`rustc-flux`) and making a git commit snapshot of the repository contents.

Its intended use is as a drop-in replacement for `flux` that tracks the
repository state and flux output.

## Dependencies

- [`flux`](https://github.com/flux-rs/flux)
- A recent version of Python 3

Windows and Linux support is untested, though Linux is presumed to work.

## Installation

Add `flux-snapshot` to your path.

## Usage

By default, `flux-snapshot` will act as a wrapper around `cargo-flux`. So
for example, instead of using

```bash
cargo-flux check
```

you can use

```bash
flux-snapshot check
```

There are some additional options too.

| Flag | Argument | Description |
| ---- | -------- | ----------- |
| `-d`, `--dir` | Path | The path to run `flux-snapshot` in (defaults to current
directory) |
| `-m`, `--message` | String | The message to put in the commit created by
`flux-snapshot` (if not given, uses a default message) |
|`--rustc` | None | Run `rustc-flux` instead of `cargo-flux` |

## Output buffering

Right now `flux-snapshot` hangs until the `flux` subprocess finishes outputting
before it reflects that output. I'm sure there's a way to get it to
tee its output properly but I'm not bothered enough to fix it.
