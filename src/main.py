from io import StringIO
import zipfile
import random
import statistics
import argparse
import logging

import requests
import pandas as pd
import numpy as np
from sklearn.metrics import brier_score_loss

import settings


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def download_zip_from_url(url, target_file, chunk_size=100):
    """Download zip from url to target file"""

    response = requests.get(url, stream=True)
    with open("/tmp/economist.zip", "wb") as fd:
        for chunk in response.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

    logging.info("Downloaded economist model to /tmp/economist.zip")


def get_538_df(url):
    """Get dataframe of 538 predictions"""

    response = requests.get(url)
    response_text = response.text
    data = StringIO(response_text)
    return pd.read_csv(data)


def get_economist_df(url):
    """Get dataframe of economist predictions"""

    download_zip_from_url(url, "/tmp/economist.zip")

    with zipfile.ZipFile("/tmp/economist.zip", "r") as z:
        z.extractall("/tmp")

    return pd.read_csv(
        "/tmp/output/site_data/state_averages_and_predictions_topline.csv"
    )


def get_538_array(df, state_to_abbrev=settings.state_to_abbrev):
    """Get array of 538 predictions in order by state abbreviation"""

    most_recent_model = df["modeldate"].max()
    df = df[df["modeldate"] == most_recent_model]
    df = df[df["state"].isin(state_to_abbrev)]
    df = df.replace({"state": state_to_abbrev})
    df = df.sort_values("state")
    return df["winstate_chal"].to_numpy()


def get_economist_array(df, state_to_abbrev=settings.state_to_abbrev):
    """Get array of economist predictions in order by state abbreviation"""

    df = df.sort_values("state")
    return df["projected_win_prob"].to_numpy()


def get_outcome(dem_win_by_state=settings.dem_win_by_state):
    """Get election outcome"""

    outcome = []
    for state in dem_win_by_state:
        if state[1] < random.random():
            outcome.append(0)
        else:
            outcome.append(1)

    return np.array(outcome)


def get_brier_scores(test_array, trials):
    """Get brier scores"""

    scores = []
    for x in range(trials):
        outcome = get_outcome()
        score = brier_score_loss(outcome, test_array)
        scores.append(score)

    return scores


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trials", dest="trials", type=int, required=True, help="Trials to run",
    )
    args = parser.parse_args()

    df_538 = get_538_df(settings.url_538)
    df_economist = get_economist_df(settings.url_economist)

    array_538 = get_538_array(df_538)
    array_economist = get_economist_array(df_economist)

    scores_538 = get_brier_scores(array_538, args.trials)
    scores_economist = get_brier_scores(array_economist, args.trials)

    mean_538 = statistics.mean(scores_538)
    mean_economist = statistics.mean(scores_economist)

    pstdev_538 = statistics.pstdev(scores_538)
    pstdev_economist = statistics.pstdev(scores_economist)

    logging.info(f"538 mean, pdstev: {mean_538}, {pstdev_538}")
    logging.info(f"economist mean, pdstev: {mean_economist}, {pstdev_economist}")
