all: clean build

clean:
	rm -f *.aux *.bcf *.log *.nav *.out *.pdf *.run.xml *.snm *.toc *.vrb
	rm -rf _minted-main

c:
	rm -f *.aux *.bcf *.log *.nav *.out *.run.xml *.snm *.toc *.vrb
	rm -rf _minted-main

fast:
	pdflatex -shell-escape -interaction=nonstopmode -file-line-error main.tex

build:
	pdflatex -shell-escape -interaction=nonstopmode -file-line-error main.tex
	biber main
	pdflatex -shell-escape -interaction=nonstopmode -file-line-error main.tex
	pdflatex -shell-escape -interaction=nonstopmode -file-line-error main.tex


.PHONY: clean build all
