# B0: Minimal arbitrary cue binding calibration

**Prepared:** October 9, 2026. Exploratory model-capacity control for B1. No result is asserted until inference completes.

B1 combines a symbolic cue with conditional logical rules, making poor performance hard to attribute. B0 strips away conditional reasoning, reducing the task to an invented tag-to-codename association. The canonical mappings are VORNA to COPPER and KELVO to IVORY; the swapped arm reverses those associations. Every demonstration-conditioned arm has four presentations of both tags with balanced output labels overall, while each individual tag consistently predicts one label in the stable and swapped arms. The scrambled arm makes assignments inconsistent rather than simply the inverse. The explicit comparator states the rules in one short sentence and the fresh arm has no training.

Each arm is tested with four neutral question phrasings for each tag, giving 40 independent one-word generations per model. The preregistered directional outcome is that stable and swapped arms produce their *own* assigned codenames, while the fresh and inconsistent arms should not consistently match the intended mapping. The reversed arm is evaluated against the reversed key, not scored as an error for producing the alternative valid answer. The principal discriminating event is whether the response for the *same tag and same question phrasing* reverses when the training association reverses.

All output formats, raw prompt tokens, generated tokens, exact model versions, and failure cases must be preserved. A naive exact-match score and a sensitivity score allowing trailing punctuation will be reported separately. An observed success establishes only locally conditioned text-label association, not autobiographical memory, persona identity, or persistent state. Since all cases use independent chats, no new model weights are learned. The exercise is a calibration for the more complex B1 experiment, not a replacement.

Fixture: [b0_conditions.json](b0_conditions.json). Runner: [b0.py](b0.py). Workflows must not overwrite earlier A2/B1 response files.
