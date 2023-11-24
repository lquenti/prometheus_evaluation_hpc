all: clean
	sudo ./build_singularity.sh ./PrometheusSingleNode.Dockerfile

clean:
	sudo rm -rf ./tmp ./data ./docker* ./singularity*

.PHONY: all clean sandbox
