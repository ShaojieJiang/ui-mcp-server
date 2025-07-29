lint:
	ruff check .
	mypy ui_mcp_server
	ruff format . --check

format:
	ruff format .
	ruff check . --select I001 --fix
	ruff check . --select F401 --fix
	cd examples/frontend/react && [ -d node_modules ] || npm install
	cd examples/frontend/react && npm run format

test:
	pytest --cov --cov-report term-missing tests/

doc:
	mkdocs serve --dev-addr=0.0.0.0:8080

demo-backend:
	langgraph dev

demo-streamlit:
	streamlit run examples/frontend/streamlit/main.py

install-backend:
	uv pip install -r examples/backend/requirements.txt

install-streamlit:
	uv pip install -r examples/frontend/streamlit/requirements.txt

install-react:
	cd examples/frontend/react && npm install

demo-react:
	cd examples/frontend/react && npm run dev
