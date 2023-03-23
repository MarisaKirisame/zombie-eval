.PHONY: nightly

nightly:
	python3 python/nightly.py

clean:
	rm -rf _build third_party
