.PHONY: build build-copilot build-claude-code clean

build:
	python build.py

build-copilot:
	python build.py copilot

build-claude-code:
	python build.py claude-code

clean:
	rm -rf dist/
