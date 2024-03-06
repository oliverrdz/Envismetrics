## Env

```
python3 -m venv myenv2
source myenv2/bin/activate

pip install flask gunicorn pandas numpy scikit-learn scipy openpyxl matplotlib
```

# Run

```
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

