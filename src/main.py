import zipfile
import random
import argparse

import pandas as pd
import numpy as np
from sklearn.metrics import brier_score_loss

import settings


def get_economist_df(file):
    """Get dataframe of economist zip file"""

    with zipfile.ZipFile(file, "r") as z:
        z.extractall("/tmp")

    return pd.read_csv(
        "/tmp/output/site_data/state_averages_and_predictions_topline.csv"
    )


def get_538_array(df, state_to_abbrev=settings.state_to_abbrev):
    """Get array of 538 predictions in order by state abbreviation"""

    df = df[df["modeldate"] == "11/2/2020"]
    df = df[df["state"].isin(state_to_abbrev)]
    df = df.replace({"state": state_to_abbrev})
    df = df.sort_values("state")
    return df["winstate_chal"].to_numpy()


def get_economist_array(df, state_to_abbrev=settings.state_to_abbrev):
    """Get array of economist predictions in order by state abbreviation"""

    df = df.sort_values("state")
    return df["projected_win_prob"].to_numpy()


def get_brier_scores(
    test_array, dem_win_by_state=settings.dem_win_by_state, decimals=3
):
    """Get brier score"""

    outcome = [state[1] for state in dem_win_by_state]
    return round(brier_score_loss(outcome, test_array), decimals)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv_538",
        dest="csv_538",
        required=True,
    )
    parser.add_argument(
        "--economist_zip",
        dest="economist_zip",
        required=True,
    )
    args = parser.parse_args()

    df_538 = pd.read_csv(args.csv_538)
    df_economist = get_economist_df(args.economist_zip)

    array_538 = get_538_array(df_538)
    array_economist = get_economist_array(df_economist)

    assert len(array_538) == 51
    assert len(array_economist) == 51

    score_538 = get_brier_scores(array_538)
    score_economist = get_brier_scores(array_economist)

    print(f"538 score: {score_538}")
    print(f"Economist score: {score_economist}")
