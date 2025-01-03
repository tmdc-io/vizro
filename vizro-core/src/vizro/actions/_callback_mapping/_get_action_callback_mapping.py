"""Creates action_callback_mapping to map callback arguments to action functions."""

from typing import Any, Union

from dash import dcc
from dash.dependencies import DashDependency

from vizro.actions import export_data, filter_interaction
from vizro.actions._callback_mapping._callback_mapping_utils import (
    _get_action_callback_inputs,
    _get_action_callback_outputs,
    _get_export_data_callback_components,
    _get_export_data_callback_outputs,
)
from vizro.actions._filter_action import _filter
from vizro.actions._on_page_load_action import _on_page_load
from vizro.actions._parameter_action import _parameter
from vizro.models import Action


def _get_action_callback_mapping(action: Action, argument: str) -> Union[list[dcc.Download], dict[str, DashDependency]]:
    """Creates mapping of action name and required callback input/output."""
    action_function = action.function._function

    action_callback_mapping: dict[str, Any] = {
        export_data.__wrapped__: {
            "inputs": _get_action_callback_inputs,
            "components": _get_export_data_callback_components,
            "outputs": _get_export_data_callback_outputs,
        },
        _filter.__wrapped__: {
            "inputs": _get_action_callback_inputs,
            "outputs": _get_action_callback_outputs,
        },
        filter_interaction.__wrapped__: {
            "inputs": _get_action_callback_inputs,
            "outputs": _get_action_callback_outputs,
        },
        _parameter.__wrapped__: {
            "inputs": _get_action_callback_inputs,
            "outputs": _get_action_callback_outputs,
        },
        _on_page_load.__wrapped__: {
            "inputs": _get_action_callback_inputs,
            "outputs": _get_action_callback_outputs,
        },
    }
    action_call = action_callback_mapping.get(action_function, {}).get(argument)
    default_value: Union[list[dcc.Download], dict[str, DashDependency]] = [] if argument == "components" else {}
    return default_value if not action_call else action_call(action=action)
