# Installing and developping Pulser on Apple Silicon M series chips

Packages in the depency tree of Pulser do not all work out of the box on ARM architecture, at least for the version specified by Pulser's requirements.

For example, a known issue is that the `numpy` version required by `qutip` current release 4.6.2 does not run on ARM.
This issue should be fixed in qutip next realease. For the moment, the workaround is to use the development branch of qutip and installing it in your virtual environment before pulser.

## With `pip`

```bash
pip install https://github.com/qutip/qutip/archive/master.zip

# for usage
pip install pulser

# for development
git clone https://github.com/pasqal-io/Pulser.git
cd Pulser
git switch develop
pip install -e .
pip install -r requirements.txt
```

## With poetry

The following setup for `pyproject.toml` is known to work

```toml
# for usage
[tool.poetry.dependencies]
python = "^3.9"
pulser = "^0.4.2"
scipy = { version = "^1.7", python = ">=3.9,<3.11" }
qutip = { git = "https://github.com/qutip/qutip.git" }
```

And for development, clone the repo, set the `pyproject.toml` with

```toml
# for development
[tool.poetry.dependencies]
python = "3.9"
scipy = { version = "^1.7", python = ">=3.9,<3.11" }
qutip = { git = "https://github.com/qutip/qutip.git" }

[tool.poetry.dev-dependencies]
pulser = { path = "Pulser"}
```

and then run

```bash
poetry add "black[jupyter]" flake8 flake8-docstrings mypy pytest pytest-cov ipykernel
```

Note however that poetry takes a long time to resolve dependencies with this setup.
