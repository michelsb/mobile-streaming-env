MININET_CON = containernet/*.py
TEST = containernet/test/*.py
EXAMPLES = containernet/examples/*.py
MN = bin/mn
PYTHON ?= python3
PYMN = $(PYTHON) -B bin/mn
BIN = $(MN)
PYSRC = $(MININET_CON) $(TEST) $(EXAMPLES) $(BIN)
MNEXEC = mnexec
MANPAGES = mn.1 mnexec.1
P8IGN = E251,E201,E302,E202,E126,E127,E203,E226
PREFIX ?= /usr
BINDIR ?= $(PREFIX)/bin
MANDIR ?= $(PREFIX)/share/man/man1
DOCDIRS = doc/html doc/latex
PDF = doc/latex/refman.pdf

CFLAGS += -Wall -Wextra

all: codecheck test

clean:
	rm -rf build dist *.egg-info *.pyc $(MNEXEC) $(MANPAGES) $(DOCDIRS)

codecheck: $(PYSRC)
	-echo "Running code check"
	util/versioncheck.py
	pyflakes $(PYSRC)
	pylint --rcfile=.pylint $(PYSRC)
#	Exclude miniedit from pep8 checking for now
	pep8 --repeat --ignore=$(P8IGN) `ls $(PYSRC) | grep -v miniedit.py`

errcheck: $(PYSRC)
	-echo "Running check for errors only"
	pyflakes $(PYSRC)
	pylint -E --rcfile=.pylint $(PYSRC)

test: $(MININET_CON) $(TEST)
	-echo "Running tests"
	containernet/test/test_nets.py
	containernet/test/test_hifi.py

slowtest: $(MININET_CON)
	-echo "Running slower tests (walkthrough, examples)"
	containernet/test/test_walkthrough.py -v
	containernet/examples/test/runner.py -v

mnexec: mnexec.c $(MN) containernet/net.py
	cc $(CFLAGS) $(LDFLAGS) -DVERSION=\"`PYTHONPATH=. $(PYMN) --version`\" $< -o $@

install-mnexec: $(MNEXEC)
	install -D $(MNEXEC) $(BINDIR)/$(MNEXEC)

install-manpages: $(MANPAGES)
	install -D -t $(MANDIR) $(MANPAGES)

install: install-mnexec install-manpages
	$(PYTHON) setup.py install

develop: $(MNEXEC) $(MANPAGES)
# 	Perhaps we should link these as well
	install $(MNEXEC) $(BINDIR)
	install $(MANPAGES) $(MANDIR)
	$(PYTHON) setup.py develop

man: $(MANPAGES)

mn.1: $(MN)
	PYTHONPATH=. help2man -N -n "create a Mininet network." \
	--no-discard-stderr "$(PYMN)" -o $@

mnexec.1: mnexec
	help2man -N -n "execution utility for Mininet." \
	-h "-h" -v "-v" --no-discard-stderr ./$< -o $@

.PHONY: doc

doc: man
	doxygen doc/doxygen.cfg
	make -C doc/latex
