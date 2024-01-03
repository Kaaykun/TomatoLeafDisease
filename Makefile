.DEFAULT_GOAL := default

#################### PACKAGE ACTIONS ###################
install_package:
	@pip uninstall -y TomatoLeafDisease || :
	@pip install -e .

dowload_data:
	python main.py

run-fastapi:
	cd fastapi && uvicorn main:app --reload

run-streamlit:
	cd streamlit && streamlit run app.py
