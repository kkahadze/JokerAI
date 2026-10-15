# Retired code and model artifact

Version 0.1 removes the unused `models/finalized_model.sav` binary (59,491,671
bytes) from the current tree. It is a historical pickled model built by the old
notebook, not a model compatible with the current agent API. No supported runtime
code loaded it. No replacement pretrained model or model-quality claim is made.

The original remains in Git history at commit:

`003390b3b846cd7945285908e3a5c8b5a4d6de54`

Its SHA-256 is:

`4068554f90150385575f27106df3d02b92662666ae92afb506bb07f2bb6cac44`

To recover the original bytes from a full clone without loading the pickle:

```sh
mkdir -p models
git show 003390b3b846cd7945285908e3a5c8b5a4d6de54:models/finalized_model.sav > models/finalized_model.sav
```

Pickles can execute code when loaded. Recovery above only writes the bytes;
reconstructing the historical model environment is outside the supported API.
Future trained artifacts belong in versioned external storage or release assets,
with training configuration, dependency versions and checksums. Model extensions
are ignored to prevent accidental recommits.

The commented-out `src/joker.py`, obsolete `src/simulation.py`, incompatible
ASCII `src/display.py`, and empty `projects/JokerAI` file were also retired.
Their originals are recoverable at the same commit. The supported CLI replaces
the old simulation entry point.

History has not been rewritten. A full clone will still download the historical
binary; a shallow clone of the cleaned default branch avoids it.
