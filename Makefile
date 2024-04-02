BASE_URL = http://localhost:8000/
ENDPOINTS = test test-async test-async2 test-async3 test-async4
API_ENDPOINTS = $(addprefix $(base_url),$(endpoints))

.PHONY: benchmark-endpoint
benchmark-endpoint:
	@echo "Benchmarking endpoint $(url)..."
	ab -n 1000 -c 50 -s 120 -p benchmark/post.json -T application/json $(url) >> benchmark/$(file).txt;

.PHONY: requirements
requirements:
	pip-compile --output-file requirements.txt --quiet requirements.in
	pip-sync requirements.txt

.PHONY: local-server
local-server:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1

.PHONY: benchmark
benchmark:
	@echo "Starting benchmark for the following endpoints $(ENDPOINTS) ..."
	@$(foreach endpoint,$(ENDPOINTS), make -s benchmark-endpoint url=$(addprefix $(BASE_URL),$(endpoint)) file=$(endpoint);)