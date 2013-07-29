clean:
	rm -rf build/ dist/ marcx.egg-info/
	find . -name "*pyc" -exec rm -rf {} \;