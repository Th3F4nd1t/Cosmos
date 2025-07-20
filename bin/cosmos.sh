echo "wip, don't work cuz no venv being setup by script. will add this to setup.sh and check a is_setup.tx file in the bin to see if it is able to use venv otherwise it'll stop cuz lowk idc"



if ! (pip3 install -r ../requirements.txt > /dev/null 2>&1 || pip install -r ../requirements.txt > /dev/null 2>&1);
	then echo "Something went wrong with installing requirements. "; fi

