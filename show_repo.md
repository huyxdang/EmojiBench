# Public Repo Scope

Goal: publish only the fixed benchmark dataset and the code needed to run, score, and plot local model results. Do not check in model outputs or old judge artifacts.

Reproducibility target: a fresh checkout should be able to install dependencies, run the fixed 100-example dataset through the supported providers, score local predictions deterministically, and generate local plots. The public repo does not need to reproduce dataset generation. Exact hosted-model outputs may still vary if provider aliases or serving behavior change.

## Include

```text
artifacts/emoji-bench-dataset-100/
emoji_bench/
emoji_bench/scoring/
scripts/evaluate_continuation.py
scripts/score_continuation.py
scripts/plot_final_answer.py
run.sh
requirements.txt
pyproject.toml
uv.lock
README.md
LICENSE
.gitignore
.env.example
```

`run.sh` needs the three scripts above:

```text
scripts/evaluate_continuation.py
scripts/score_continuation.py
scripts/plot_final_answer.py
```

Those scripts import the `emoji_bench/` package, so the package must stay with them.

Keep `matplotlib` in `requirements.txt` because `scripts/plot_final_answer.py` uses it.

Keep `uv.lock` or pin `requirements.txt` tightly if the public repo should be dependency-reproducible, not just code-reproducible.

## Exclude

```text
artifacts/evals/
artifacts/evals-clean/
artifacts/plots/
public/
index.html
note.md
note2.md
scripts/judge_continuation.py
judge.jsonl
nested_scores.jsonl
```

Do not include checked-in model outputs, generated score summaries, generated plots, or old LLM-as-judge artifacts.

## Cleanup Before Publishing

- Removed `scripts/judge_continuation.py` and the `emoji_bench/judge/` package.
- Refactored `scripts/score_continuation.py` so final-answer scoring no longer imports judge artifact plumbing.
- Moved final-answer scoring helpers into `emoji_bench/scoring/continuation_scorer.py`.
- Renamed `scripts/plot_b_final_answer.py` to `scripts/plot_final_answer.py` and updated `run.sh` to call the new name.
- Removed checked-in `artifacts/evals*`, `artifacts/plots`, old site files, notes, tests, and dataset-generation code.
- Updated `README.md` to say users generate outputs locally under `artifacts/evals/` and plots under `artifacts/plots/`.
- Kept `.env.example` so users can see the expected provider API key names.

## Repo Story

The public repo should provide:

- the fixed 100-example dataset,
- scripts to run models on the default benchmark condition,
- deterministic final-answer scoring,
- optional final-answer plots generated from local results.

It should not provide:

- dataset generation reproducibility,
- our leaderboard result artifacts,
- old LLM-as-judge outputs,
- judge-backed scoring as part of the main benchmark path.
