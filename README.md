# UWin Success Backend

## Setting up the project

You will need to use a virtual environment to run the project. To set up the virtual environment and install the requirements, run the following commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the project

To run the project, run the following command:

```bash
uvicorn main:app --reload
```