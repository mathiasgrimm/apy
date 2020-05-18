clear;
find . -name '*.pyc' -delete


clear;python -m pytest -s -v --cov=apy --cov-report html -c pytest.ini