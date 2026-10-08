# AI use and personal verification

Codex drafted the protocol, code, method explanations, and report structure after a ChatGPT
conversation helped select the dataset. The human requested an opening abstract with actual
experimental results. Abstract numbers are populated from the saved run, not invented.

| Suggestion or choice | Decision and reason | Verification status |
|---|---|---|
| Restrict analysis to one species and one outcome | Accepted: Adelie body mass keeps the comparison focused | Student source check pending |
| Use a 200 g meaningful difference | Explicit teaching assumption; not claimed as a biological standard | Student should assess and acknowledge the rationale |
| Compare Welch and within-group bootstrap intervals | Accepted; both require independence and suitable sampling | Assistant code compares Welch output with SciPy |
| Compute power from the observed effect | Not used; effect/noise/sample-size grids were fixed separately | Protocol file and simulated truth are inspectable |
| Simulate correlated records | Accepted to isolate an independence violation while preserving marginal variance | Model and design-effect derivation are in the notebook |
| Treat significant sex differences as causal | Not adopted; sex was not randomized and sampling remains limited | Student interpretation pending |

## Complete personally before submission

- Name and verification date: TODO
- Original source checked, with file/section and what I confirmed: TODO
- One interval or simulation quantity checked independently, with method and result: TODO
- Advice I accepted/rejected and my reason: TODO
- An unexpected, null, or assumption-challenging result and its implication: TODO
- My conclusion and the population to which I believe it applies: TODO

Assistant validation is separate from these entries. Do not mark verification complete unless
you actually performed it. For example, independently derive the baseline sampling standard
deviation or reproduce a two-group interval with a separate tool and document the result.
