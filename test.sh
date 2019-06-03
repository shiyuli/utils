# check types
mypy core
mypy test.py

# remove mypy caches
find . -name ".mypy_cache" -type d -delete

# python test
python test.py
