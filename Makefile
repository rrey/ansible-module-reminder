REPO=$(shell git rev-parse --show-toplevel)

check:
	$(REPO)/tools/start_api.sh
	ansible-playbook -i test.ini test.yml
