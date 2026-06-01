# cobel results — planner=claude mode=few-shot samples=3

## (a) Headline — schema validity (the demand-side claim)

| task | mode | schema_ok | pass@1 | pass@k |
|---|---|---|---|---|
| latch-buckle | few-shot | ok | 1 | 3/3 |
| pour | few-shot | ok | 1 | 3/3 |
| relocate-part | few-shot | ok | 1 | 3/3 |
| seat-fuse | few-shot | ok | 1 | 3/3 |
| sort-by-weight | few-shot | ok | 1 | 3/3 |
| stack-blocks | few-shot | ok | 1 | 3/3 |

## (b) Retarget outcomes (engine-coverage map)

| task | mode | allegro | leap | pneumatic-6f |
|---|---|---|---|---|
| latch-buckle | few-shot | beyond_engine | beyond_engine | beyond_engine |
| pour | few-shot | beyond_engine | beyond_engine | beyond_engine |
| relocate-part | few-shot | beyond_engine | beyond_engine | beyond_engine |
| seat-fuse | few-shot | retarget_ok | retarget_ok | retarget_ok |
| sort-by-weight | few-shot | beyond_engine | beyond_engine | beyond_engine |
| stack-blocks | few-shot | beyond_engine | beyond_engine | beyond_engine |
