# brier
This repo can be used to compare the FiveThirtyEight presidential election model to the Economist model.
The repo was inspired by the post here: https://www.metaculus.com/questions/5503/comparing-538-and-economist-forecasts-in-2020/.
To run the comparison, you need to download the predictions at: https://easyupload.io/sk8kiw.
Then pass the input files to the program like this:
```shell
python3 src/main.py \
  --economist_zip=/tmp/economist_model_output.zip \
  --csv_538=/tmp/538_state_toplines.csv
```
Remember, the lower score wins!
