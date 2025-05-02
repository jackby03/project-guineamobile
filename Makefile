# Minimal makefile for Sphinx documentation

# Variables configurables
SPHINXOPTS    ?=
SPHINXBUILD   = .venv\Scripts\sphinx-build
SOURCEDIR     = docs/source
BUILDDIR      = docs/build

# Ayuda: muestra las opciones disponibles
help:
    @$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Objetivo principal: construir la documentación en HTML
html:
    @$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

# Limpiar los archivos generados
clean:
    @echo "Limpiando el directorio de construcción..."
    @rm -rf "$(BUILDDIR)"

# Catch-all target: redirige todos los objetivos desconocidos a Sphinx
%: Makefile
    @$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)