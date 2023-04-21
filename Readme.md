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
