SHELL:=bash
#
# Makefile for building/packaging qgis for lizmap hosting
#

VERSION=$(shell ./metadata_key ../metadata.txt version)

main:
»   echo "Makefile for packaging infra components: select a task"

PACKAGE=qgis-wmsGetFeatureInfoPrecision
FILES = ../*.py ../metadata.txt ../README.md
PACKAGEDIR=wmsGetFeatureInfoPrecision

build/$(PACKAGEDIR):
	@rm -rf build/$(PACKAGEDIR)
	@mkdir -p build/$(PACKAGEDIR)


.PHONY: package
package: build/$(PACKAGEDIR)
	@echo "Building package $(PACKAGE)"
	@cp -rLp $(FILES) build/$(PACKAGEDIR)/
	$(FACTORY_SCRIPTS)/make-package $(PACKAGE) $(VERSION) $(PACKAGEDIR) ./build

test:
	$(MAKE) -C tests

version:
	@echo $(VERSION)

