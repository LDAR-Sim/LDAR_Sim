import pandas as pd
from file_processing.output_processing.summary_output_manager import SummaryOutputManager


def mock_summary_output_manager_init(self):
    return


def test_combine_outputs_when_old_outputs_empty(mocker):
    mocker.patch.object(SummaryOutputManager, "__init__", mock_summary_output_manager_init)
    output_manager: SummaryOutputManager = SummaryOutputManager()
    old_outputs = {"output1": pd.DataFrame(), "output2": pd.DataFrame()}
    new_outputs = {
        "output1": [pd.DataFrame({"A": [1, 2, 3]}), pd.DataFrame({"A": [4, 5, 6]})],
        "output2": [pd.DataFrame({"B": [7, 8, 9]}), pd.DataFrame({"B": [10, 11, 12]})],
    }
    expected_outputs = {
        "output1": pd.DataFrame({"A": [1, 2, 3, 4, 5, 6]}),
        "output2": pd.DataFrame({"B": [7, 8, 9, 10, 11, 12]}),
    }
    combined = output_manager.combine_outputs(old_outputs, new_outputs)
    for key in combined.keys():
        assert combined[key].equals(expected_outputs[key])


def test_combine_outputs_when_old_outputs_not_empty(mocker):
    mocker.patch.object(SummaryOutputManager, "__init__", mock_summary_output_manager_init)
    output_manager: SummaryOutputManager = SummaryOutputManager()
    old_outputs = {
        "output1": pd.DataFrame({"A": [1, 2, 3]}),
        "output2": pd.DataFrame({"B": [4, 5, 6]}),
    }
    new_outputs = {
        "output1": [pd.DataFrame({"A": [7, 8, 9]}), pd.DataFrame({"A": [10, 11, 12]})],
        "output2": [pd.DataFrame({"B": [13, 14, 15]}), pd.DataFrame({"B": [16, 17, 18]})],
    }
    expected_outputs = {
        "output1": pd.DataFrame({"A": [1, 2, 3, 7, 8, 9, 10, 11, 12]}),
        "output2": pd.DataFrame({"B": [4, 5, 6, 13, 14, 15, 16, 17, 18]}),
    }
    combined = output_manager.combine_outputs(old_outputs, new_outputs)
    for key in combined.keys():
        assert combined[key].equals(expected_outputs[key])
