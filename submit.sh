#!/bin/sh

mark="$1"
ds_name="ds004186"
repo="$HOME/scratch/$ds_name.git"
dest="$SLURM_TMPDIR/$ds_name"

git clone "$repo" "$dest"

rm -f data/"$mark"
ln -s "$dest" data/"$mark"

pytest tests -m "$mark" --benchmark-save="$mark"

rm -f data/"$mark"