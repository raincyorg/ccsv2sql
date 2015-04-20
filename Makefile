#
# Makefile to build standalone `ccsv2sql` Unix-like executable program.
#

FREEZE = cxfreeze
SOURCE = ccsv2sql.py
TARGET = ccsv2sql

make:
	$(FREEZE) $(SOURCE) --target-dir dist
	
dependencies:
	pip -q install cx_Freeze
	
test:
	sudo mv dist/${TARGET} /usr/bin 
	$(TARGET) -l -f sample.csv
	cat sample.sql

clean:
	rm -r -f dist
	rm -r -f $(TARGET)
