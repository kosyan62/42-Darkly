VENV       := venv
PYTHON     := $(VENV)/bin/python3
PIP        := $(VENV)/bin/pip
EXPLOITS   := brute_force file_upload form_validation header_spoofing hidden_path sqli_images sqli_members

.PHONY: all setup clean fclean re help $(EXPLOITS)

help:
	@echo "Usage: make VM_IP=<ip> [target]"
	@echo ""
	@echo "Targets:"
	@echo "  all              Run all exploits"
	@echo "  setup            Create venv and install dependencies"
	@echo "  clean            Remove __pycache__ directories"
	@echo "  fclean           Remove venv and __pycache__"
	@echo "  re               Rebuild and run all"
	@echo ""
	@echo "Individual exploits:"
	@for e in $(EXPLOITS); do echo "  $$e"; done

all: setup
ifndef VM_IP
	$(error VM_IP is not set. Usage: make VM_IP=<ip> [target])
endif
	@for exploit in $(EXPLOITS); do \
		echo ""; \
		echo "=== $$exploit ==="; \
		script=$$(ls $$exploit/Resources/*.py 2>/dev/null | head -1); \
		if [ -n "$$script" ]; then \
			$(PYTHON) "$$script" || echo "[FAILED]"; \
		else \
			echo "[NO SCRIPT]"; \
		fi; \
	done

setup: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -q -r requirements.txt
	touch $(VENV)/bin/activate

$(EXPLOITS): setup
ifndef VM_IP
	$(error VM_IP is not set. Usage: make VM_IP=<ip> $@)
endif
	@echo "=== $@ ==="
	@$(PYTHON) $$(ls $@/Resources/*.py | head -1)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

fclean: clean
	rm -rf $(VENV)

re: fclean all
