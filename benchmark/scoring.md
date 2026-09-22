# Benchmark Scoring

## Static score — /40

- API names backed by catalog/docs: 10
- effects/failure correctness: 8
- lifecycle considerations: 6
- async lifetime: 4
- architecture/state ownership: 6
- no unsupported confidence claims: 6

## Compile score — /25

- UEFN compilation succeeds: 25

No partial compile score for "looks compilable".

## Runtime score — /20

- expected behavior observed: 12
- cleanup/lifecycle observed: 4
- logs free of relevant runtime errors: 4

## Multiplayer score — /15

- concurrent players tested: 8
- leave/respawn/late join tested where relevant: 7

## Maximum

100.

A static-only run cannot exceed 40.
