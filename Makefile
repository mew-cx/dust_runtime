# github.com/mew-cx/dust_devel/Makefile

# the default target
.PHONY: all
all:
	echo "default target not yet defined"

# clean out pycache cruft
.PHONY: clean
clean:
	find . -depth -type d -name __pycache__ -exec rm -rf {} \;

# vim: set sw=4 ts=8 noet ic ai:
