SHELL := /bin/bash


OLLAMA_MODEL := llama3.1 #llava
VLLM_MODEL := neuralmagic/Meta-Llama-3.1-8B-Instruct-quantized.w4a16 #neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8

# https://ollama.com/
# https://github.com/ollama/ollama
run-ollama-gpu:
	@docker run --rm \
	-d \
	--name ollama \
	--gpus all \
	-v ollama:/root/.ollama \
	-p 11434:11434 \
	-e OLLAMA_FLASH_ATTENTION=1 \
	ollama/ollama:0.3.6
	@docker exec -it ollama ollama pull $(OLLAMA_MODEL)
	@docker logs ollama -f

run-ollama-cpu:
	@docker run --rm \
	-d \
	--name ollama \
	-v ollama:/root/.ollama \
	-p 11434:11434 \
	ollama/ollama:0.3.6
	@docker exec -it ollama ollama pull $(OLLAMA_MODEL)
	@docker logs ollama -f

stop-ollama:
	@docker stop ollama

# https://docs.vllm.ai/en/latest/index.html
# https://github.com/vllm-project/vllm
run-vllm-gpu:
	@docker run --rm \
	--name vllm \
	--gpus all \
	-v vllm:/root/.cache/huggingface \
	-p 8000:8000 \
	vllm/vllm-openai:v0.5.5 \
	--model $(VLLM_MODEL) \
	--gpu-memory-utilization 0.5 \
	--max-model-len 4096

# run-vllm-cpu
## https://github.com/vllm-project/vllm/blob/main/Dockerfile.cpu


# https://github.com/open-webui/open-webui
# https://docs.openwebui.com/
run-webui:
	@docker compose up

rm-webui:
	@docker compose down -v
