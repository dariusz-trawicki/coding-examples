
### Run

```bash
conda create -p ./venv python=3.12 -y
conda activate ./venv
pip install -r requirements.txt
```


### Clean up
```bash
conda deactivate
conda remove -p ./venv --all -y
```