pushd ~/Desktop  # TODO: make this configurable

mkdir $1
cd $1

# Create basic SystemVerilog project
mkdir src
touch src/top.sv
touch src/top_tb.sv


git init
git add .
git commit -am "Initial Commit"

popd