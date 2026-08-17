# ADTF Metadata & Field Reference

## metadata.json

```json
{
  "team_id": "team-ecoinfrahub",
  "domain": "math_scientific_reasoning",
  "language_scope": [
    "en"
  ],
  "african_alpha_claim": false,
  "budget_laptop_claim": true,
  "submitter": {
    "name": "Ibrahim Ismaila",
    "email": "ecoinboxhub@gmail.com",
    "github_handle": "ecoinboxhub"
  },
  "cross_disciplinary_pairing": {
    "discipline": "civil_engineering",
    "load_bearing": true,
    "description": "The model applies mathematical and scientific reasoning to real-world African infrastructure challenges, including civil engineering, transportation, drainage, stormwater, pavement analysis, and related infrastructure problems."
  },
  "test_prompts": [
    {
      "prompt_id": "eco-01",
      "prompt": "What is the standard pavement structure for a rural road in Nigeria according to the Nigerian Highway Manual? Describe the typical layers and their thickness."
    },
    {
      "prompt_id": "eco-02",
      "prompt": "Explain the Rational Method for calculating stormwater runoff. What parameters are needed and how is the peak flow rate determined?"
    }
  ],
  "model": {
    "name": "Qwen2.5-3B-Instruct",
    "runtime": "llama.cpp",
    "quantization": "GGUF Q4_K_M",
    "parameters_estimate": "3B",
    "packaging": "binary_bundle"
  },
  "_runtime": {
    "model_path": "model/ecoinframind-ai-model.gguf",
    "context_length": 4096,
    "max_tokens": 512
  }
}
```

## ADTF Field Reference

| Field                                     | Required | Current Value                      | Status   | Reference / Requirement                                              |
| ----------------------------------------- | -------- | ---------------------------------- | -------- | -------------------------------------------------------------------- |
| `team_id`                                 | ✅        | `team-ecoinfrahub`                 | ✅ Valid  | Unique registered team ID                                            |
| `domain`                                  | ✅        | `math_scientific_reasoning`        | ✅ Valid  | Must be exactly `math_scientific_reasoning`                          |
| `language_scope`                          | ✅        | `["en"]`                           | ✅ Valid  | `en` is a valid BCP-47 language code                                 |
| `african_alpha_claim`                     | ✅        | `false`                            | ✅ Valid  | `false` because no African Use Case Bonus is being claimed           |
| `budget_laptop_claim`                     | ✅        | `true`                             | ✅ Valid  | Must be `true`                                                       |
| `submitter.name`                          | ✅        | `Ibrahim Ismaila`                  | ✅ Valid  | Full submitting team member name                                     |
| `submitter.email`                         | ✅        | `ecoinboxhub@gmail.com`            | ✅ Valid* | Must be linked to the registered team                                |
| `submitter.github_handle`                 | ✅        | `ecoinboxhub`                      | ✅ Valid* | Must be verifiable                                                   |
| `cross_disciplinary_pairing.discipline`   | ✅        | `civil_engineering`                | ✅ Valid  | Should identify the deep-tech discipline served                      |
| `cross_disciplinary_pairing.load_bearing` | ✅        | `true`                             | ✅ Valid  | Pairing is integral to the submission                                |
| `test_prompts`                            | ✅        | 2 prompts                          | ✅ Valid  | Exactly 2 required                                                   |
| `test_prompts[0].prompt_id`               | —        | `eco-01`                           | ✅ Valid  | Unique prompt identifier                                             |
| `test_prompts[1].prompt_id`               | —        | `eco-02`                           | ✅ Valid  | Unique prompt identifier                                             |
| `model.runtime`                           | ✅        | `llama.cpp`                        | ✅ Valid  | Must be exactly `llama.cpp`                                          |
| `model.quantization`                      | ✅        | `GGUF Q4_K_M`                      | ✅ Valid  | Accepted GGUF quantization format                                    |
| `model.parameters_estimate`               | ✅        | `3B`                               | ✅ Valid  | Approximate parameter count                                          |
| `model.packaging`                         | ✅        | `binary_bundle`                    | ✅ Valid  | Must be `docker_image`, `docker_build_from_repo`, or `binary_bundle` |
| `_runtime.model_path`                     | ✅        | `model/ecoinframind-ai-model.gguf` | ✅ Valid  | Relative path from repo root to the `.gguf` file                     |
| `_runtime.context_length`                 | —        | `4096`                             | ✅ Valid  | Kept inside `_runtime` so profiler schema validation passes           |
| `_runtime.max_tokens`                     | —        | `512`                              | ✅ Valid  | Kept inside `_runtime` so profiler schema validation passes           |

* These values must remain exactly as provided and must not be changed or guessed.