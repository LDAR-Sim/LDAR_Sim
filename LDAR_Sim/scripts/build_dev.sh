rm -rf build
mkdir -p build
cp ./src/*.py build
pipenv lock -r > requirements.txt
pip install -r requirements.txt --no-deps -t build