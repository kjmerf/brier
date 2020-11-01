# brier
This repo can be used to compare the FiveThirtyEight presidential election model to the Economist model.
The repo was inspired by the post here: https://www.metaculus.com/questions/5503/comparing-538-and-economist-forecasts-in-2020/.

To run the comparison, set the test probabilities by adjusting the ```dem_win_by_state``` dictionary in ```src/settings.py``` or accept the defaults.
Then create a virtual environment, install requirements, and run the program:
```shell
# create a virtual environment
python3 -m venv test_env
source ./test_env/bin/activate
# install requirements
pip install -r requirements.txt
# run the program
python3 src/main.py --trials 10000
```

The program generates a Brier score for each trial for each model.
The mean and standard deviation of the set of scores is logged to the terminal for each model.
