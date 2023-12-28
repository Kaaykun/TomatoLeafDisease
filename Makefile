.DEFAULT_GOAL := default

#################### PACKAGE ACTIONS ###################
reinstall_package:
	@pip uninstall -y TomatoLeafDisease || :
	@pip install -e .
