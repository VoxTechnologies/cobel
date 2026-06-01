# cobel results — planner=mock mode=spec-only samples=1

## (a) Headline — schema validity (the demand-side claim)

| task | mode | schema_ok | pass@1 | pass@k |
|---|---|---|---|---|
| latch-buckle | spec-only | ok | 1 | 1/1 |
| pour | spec-only | ok | 1 | 1/1 |
| relocate-part | spec-only | ok | 1 | 1/1 |
| seat-fuse | spec-only | ok | 1 | 1/1 |
| sort-by-weight | spec-only | ok | 1 | 1/1 |
| stack-blocks | spec-only | ok | 1 | 1/1 |

## (b) Retarget outcomes (engine-coverage map)

| task | mode | allegro | leap | pincherx-100 | pneumatic-6f |
|---|---|---|---|---|---|
| latch-buckle | spec-only | capability_rejected | capability_rejected | capability_rejected | capability_rejected |
| pour | spec-only | beyond_engine | beyond_engine | beyond_engine | beyond_engine |
| relocate-part | spec-only | retarget_ok | retarget_ok | retarget_ok | retarget_ok |
| seat-fuse | spec-only | retarget_ok | retarget_ok | capability_rejected | retarget_ok |
| sort-by-weight | spec-only | beyond_engine | beyond_engine | beyond_engine | beyond_engine |
| stack-blocks | spec-only | beyond_engine | beyond_engine | beyond_engine | beyond_engine |
