# Emoji-Bench

Emoji-Bench is a fixed 100-example benchmark for testing whether language models can recover from an incorrect prefilled derivation step when prompted only with `Please continue.`

The public repo includes the benchmark dataset and the scripts needed to run models, score predictions deterministically, and generate local final-answer plots. It does not include our model outputs, leaderboard result artifacts, LLM-as-judge artifacts, or dataset-generation code.

## Dataset

The fixed benchmark input lives at:

```text
artifacts/emoji-bench-dataset-100/
├── test.jsonl
├── manifest.json
└── README.md
```

Each `test.jsonl` row contains a three-turn continuation task:

1. `turn_1_user`: the formal emoji system, expression, and step format.
2. `turn_1_assistant_prefill`: a partial assistant derivation ending on an injected error.
3. Turn 2 is supplied by the evaluator, usually `Please continue.`

Scoring compares the model's extracted `Final Output:` against `ground_truth_final_output`.

## Setup

Requires Python `>=3.11`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set API keys for the providers you plan to run:

```bash
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GEMINI_API_KEY=...
export MISTRAL_API_KEY=...
```

Gemini and Mistral use plain HTTP from the standard library. OpenAI and Anthropic use their official SDKs.

## Run

Run the default benchmark:

```bash
./run.sh artifacts/emoji-bench-dataset-100 -- --max-concurrent 8
```

`run.sh` will:

1. Run `scripts/evaluate_continuation.py` for each configured model.
2. Write predictions under `artifacts/evals/`.
3. Score each completed cell with `scripts/score_continuation.py`.
4. Generate final-answer plots with `scripts/plot_final_answer.py`.

Generated outputs are local artifacts and are intentionally not checked in.

## Single Cell

```bash
python scripts/evaluate_continuation.py \
  artifacts/emoji-bench-dataset-100 \
  --model gpt-5.4-mini-reasoning-xhigh \
  --output-dir artifacts/evals/gpt-5.4-mini-reasoning-xhigh \
  --max-concurrent 8

python scripts/score_continuation.py \
  artifacts/evals/gpt-5.4-mini-reasoning-xhigh
```

## Score

Score an existing prediction directory:

```bash
python scripts/score_continuation.py artifacts/evals/<run-dir>
```

This writes:

```text
scores.jsonl
score_summary.json
```

The headline metric is:

| Metric | Meaning |
|---|---|
| `final_answer_correct_rate` | Extracted `Final Output:` equals `ground_truth_final_output` |

The summary also includes regex diagnostic buckets such as `detect_recover`, `silent_recovery`, `blind_wrong_branch`, and `extraction_failed`.

## Plot

Generate plots from locally scored eval directories:

```bash
python scripts/plot_final_answer.py
```

Plots are written to:

```text
artifacts/plots/
```

## Repo Map

```text
artifacts/emoji-bench-dataset-100/  fixed benchmark dataset
emoji_bench/eval/                   run paths and shared runner
emoji_bench/providers/              provider request plumbing
emoji_bench/scoring/                deterministic final-answer scoring
scripts/evaluate_continuation.py    run one model
scripts/score_continuation.py       score predictions
scripts/plot_final_answer.py        plot local score summaries
run.sh                              batch runner
```

## License

MIT. See `LICENSE`.
