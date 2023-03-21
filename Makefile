.PHONY: nightly

nightly:
	rm -rf third_party
	python3 nightly.py
