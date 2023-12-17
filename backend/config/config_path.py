import os

ABSOLUTE_ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_absolute_path(path_from_project_dir: str) -> str:
    return ABSOLUTE_ROOT_PATH + path_from_project_dir


class ConfigPath:
    KEY_FILE_PATH = get_absolute_path("/data/key.csv")
    SAMPLE_SUBMISSION_FILE_PATH = get_absolute_path("/data/sampleSubmission.csv")
    WEATHER_FILE_PATH = get_absolute_path("/data/weather.csv")
    TRAIN_EXISTING_FILE_COMBINED_PATH = get_absolute_path('/data/TRAIN_EXISTING_DF_COMBINED.csv')
    TEST_EXISTING_FILE_COMBINED_PATH = get_absolute_path('/data/TEST_EXISTING_DF_COMBINED.csv')
    TRAIN_FILE_PATH = get_absolute_path('/data/train.csv')
    TEST_FILE_PATH = get_absolute_path('/data/test.csv')





