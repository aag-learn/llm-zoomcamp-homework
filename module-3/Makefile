.PHONY: down up load_flows

up:
	@socket_path="$$(podman info --format '{{.Host.RemoteSocket.Path}}')"; \
	if [ -d "$$socket_path" ]; then \
		rmdir "$$socket_path" 2>/dev/null || { \
			echo "Expected a Podman socket at $$socket_path, but found a directory."; \
			echo "Remove it manually if it is not empty, then rerun 'make up'."; \
			exit 1; \
		}; \
	fi; \
	systemctl --user start podman.socket; \
	if [ ! -S "$$socket_path" ]; then \
		echo "Podman API socket is not available at $$socket_path."; \
		echo "Check 'systemctl --user status podman.socket' and rerun 'make up'."; \
		exit 1; \
	fi; \
	CONTAINER_SOCKET_PATH="$$socket_path" podman compose up -d --force-recreate

down:
	podman compose down
	systemctl --user stop podman.socket

load_flows:
	fish ./upload-flows.fish
