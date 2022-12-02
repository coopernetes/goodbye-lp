# Export data (properly) from LastPass
Run this script to export your data to a JSON file and convert to 1Password/BitWarden/KeePassXC.

Requires:
* Python 3
* [lastpass-cli](https://github.com/lastpass/lastpass-cli)

## Why
LastPass exports its data via CSV. If you use secure notes, you'll have no idea what your note is
for as they don't export the name (!) of the note (just the content).
