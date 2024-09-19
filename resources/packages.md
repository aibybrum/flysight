# Poetry

poetry init

## Add API dependencies

poetry add fastapi psycopg2-binary sqlalchemy uvicorn influxdb-client \
pandas numpy geopy peakutils pyproj python-dotenv utm bcrypt \
python-multipart loguru "pydantic[email]" --group api

## Add Notebook dependencies

poetry add numpy pandas plotly peakutils geopy pyproj utm seaborn pyarrow \
python-dotenv panel ipywidgets import-ipynb --group notebook

## Add Scraper dependencies

poetry add selenium --group scraper

## Commands

poetry env info
poetry env list
poetry shell

exit - deactivate

## Visualisation packages

- matplotlib
- seaborn
- plotly (mostly used) -> interactive
- mapbox 
- leafmap
- pydeck
- keplergl