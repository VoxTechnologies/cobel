# cobel results — planner=claude mode=few-shot samples=5

## (a) Headline — schema validity (the demand-side claim)

| task | mode | schema_ok | pass@1 | pass@k |
|---|---|---|---|---|
| latch-buckle | few-shot | ok | 1 | 5/5 |
| pour | few-shot | ok | 1 | 5/5 |
| relocate-part | few-shot | ok | 1 | 5/5 |
| seat-fuse | few-shot | ok | 1 | 5/5 |
| sort-by-weight | few-shot | ok | 1 | 5/5 |
| stack-blocks | few-shot | ok | 1 | 5/5 |

## (b) Retarget outcomes (engine-coverage map)

| task | mode | allegro | leap | pincherx-100 | pneumatic-6f |
|---|---|---|---|---|---|
| latch-buckle | few-shot | capability_rejected | capability_rejected | capability_rejected | capability_rejected |
| pour | few-shot | beyond_engine | beyond_engine | beyond_engine | beyond_engine |
| relocate-part | few-shot | beyond_engine | beyond_engine | beyond_engine | beyond_engine |
| seat-fuse | few-shot | retarget_ok | retarget_ok | capability_rejected | retarget_ok |
| sort-by-weight | few-shot | beyond_engine | beyond_engine | beyond_engine | beyond_engine |
| stack-blocks | few-shot | beyond_engine | beyond_engine | beyond_engine | beyond_engine |
