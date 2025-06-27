FROM python:3.12.10-slim AS pyt 

RUN pip install uv
RUN apt-get update && apt-get install -y git; apt-get install -y tree

ENV UV_LINK_MODE=copy

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR	/app 

COPY pyproject.toml uv.lock README.md .

COPY src/ ./src
COPY tests ./tests

# ENV UV_ENV_FILE="/app/.venv"

RUN uv sync --frozen

EXPOSE 8080
EXPOSE 8081
EXPOSE 8082

CMD ["uv", "run", "--frozen", "paytrack"]

