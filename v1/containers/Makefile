all: clean
	sudo ./build_singularity.sh ./PrometheusSingleNode.Dockerfile

sandbox: clean
	sudo ./build_sandbox.sh ./PrometheusSingleNode.Dockerfile

clean:
	sudo rm -rf ./tmp ./data ./docker* ./singularity*

.PHONY: all clean sandbox
