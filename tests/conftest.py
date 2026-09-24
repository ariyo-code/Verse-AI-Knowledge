# Root-level test_*.py files from V22-V24 are script-style compatibility checks
# (some intentionally raise SystemExit at import time). They continue to run
# explicitly from tools/validate_all.py; pytest collects the V25 suites below.
collect_ignore = [
    'test_api_coverage_v24.py',
    'test_claim_resolution_v24.py',
    'test_cli_contracts.py',
    'test_cli_v22.py',
    'test_cli_v23.py',
    'test_cli_v24.py',
    'test_epic_url_security.py',
    'test_generated_provenance.py',
    'test_generated_provenance_v24.py',
    'test_lab_state.py',
    'test_llm_eval_runner_v24.py',
    'test_v22_integrity.py',
    'test_v23_integrity.py',
    'test_v24_integrity.py',
]
