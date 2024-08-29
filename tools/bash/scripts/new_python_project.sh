pushd ~/Desktop  # TODO: make this configurable

mkdir $1
cd $1

# create venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install numpy pandas requests matplotlib
touch main.py
git init
git add .
git commit -am "Initial Commit"

popd