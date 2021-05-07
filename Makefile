include .env

InstallPackage:
	@sh envs/build_env.sh ${hasGPU}

BuildENV:
	sudo apt-get install -y python3-pip
	sudo python3 -m pip install virtualenv
	cd ../; virtualenv ${PROJECT_NAME}
	@echo "Please enter the command \"source bin/activate\"."

LeaveENV:
	@echo "Please enter the command \"deactivate\"."

RemoveENV:
	rm -rf bin/ lib/ include/

run:
	python src/app.py


clean_py:
	find src/ -type d -name __pycache__ -exec rm -r {} \+
	rm -rf bin/ lib/ include/ share/

Backup:
	rsync -avh ../HUMAN_detection/ jackychang@10.0.4.31:/volume1/JC_project/HUMAN_detection/
