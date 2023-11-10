.PHONY: all
all:
	@echo "available target: make clean"

.PHONY: clean
clean:
	rm -rf build/ dist/ marcx.egg-info/
	find . -name "*pyc" -exec rm -rf {} \;
	rm -rf __pycache__/

.PHONY: test
test:
	pytest -W ignore::DeprecationWarning
