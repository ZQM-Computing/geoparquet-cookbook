# Contributing to GeoParquet Patterns

Thanks for your interest in improving this project!

## Development Setup

```bash
git clone https://github.com/zqmcomputing/geoparquet-patterns.git
cd geoparquet-patterns
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/ -v
# or
python -m pytest tests/ -v
```

## Code Style

- Follow PEP 8
- Use type hints where practical
- Maximum line length: 100 characters

## Adding a New Example

1. Create a new directory under `examples/` following the naming convention `NN-topic-name/`
2. Include a `README.md` explaining the pattern and when to use it
3. Add a runnable Python script with sample data generation
4. Add corresponding tests in `tests/`

## Pull Request Process

1. Fork the repository and create a feature branch
2. Make your changes with clear commit messages
3. Ensure all tests pass (`pytest tests/ -v`)
4. Update documentation if needed
5. Submit a PR with a clear description of the change

## Reporting Issues

Please include:
- Python version and OS
- Full error traceback
- A minimal reproduction script
- Expected vs. actual behavior

## Code of Conduct

Be respectful and constructive. Harassment or discrimination will not be tolerated.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
