import copy
import json
import os
from dataclasses import dataclass, field
from functools import partial
from logging import getLogger, DEBUG
from typing import Union, NoReturn, Optional, Any, Dict, List, Type
from urllib.parse import urlparse
import pathlib

from idmtools import IdmConfigParser
from idmtools.assets import Asset
from idmtools.assets import AssetCollection
from idmtools.entities.command_line import CommandLine
from idmtools.entities.itask import ITask
from idmtools.entities.iworkflow_item import IWorkflowItem
from idmtools.entities.simulation import Simulation
from idmtools.registry.task_specification import TaskSpecification
from idmtools.utils.json import load_json_file
from idmtools.entities.iplatform import IPlatform

user_logger = getLogger('user')
logger = getLogger(__name__)

"""
Note that these 3 functions could be member functions of EMODTask but Python modules are already pretty good at being 'static classes'.
"""


def add_ep4_from_path(task, ep4_path):
    """
    Add embedded Python scripts from a given path.
    """

    for entry_name in os.listdir(ep4_path):
        full_path = os.path.join(ep4_path, entry_name)
        if(os.path.isfile(full_path) and entry_name.endswith(".py")):
            py_file_asset = Asset(full_path, relative_path="python")
            task.common_assets.add_asset(py_file_asset)

    return task

@dataclass()
class EMODTask(ITask):
    """
    EMODTask allows easy running and configuration of EMOD Experiments and Simulations
    """
    # Experiment Level Assets
    #: Eradication path. Can also be set through config file
    eradication_path: str = field(default=None, compare=False, metadata={"md": True})

    # Simulation Level Configuration objects and files
    #: Represents config.jon
    config: dict = field(default_factory=lambda: {})
    config_file_name: str = "config.json"

    #: Add --python-script-path to command line
    use_embedded_python: bool = True
    is_linux: bool = False
    implicit_configs: list = field(default_factory=lambda: [])
    use_singularity: bool = False
    sif_filename: str = None

    def __post_init__(self):
        super().__post_init__()
        self.executable_name = "Eradication"

    @classmethod
    def from_files(cls,
                   eradication_path=None,
                   config_path=None,
                   campaign_path=None,
                   demographics_paths=None,
                   ep4_path=None,
                   custom_reports_path=None,
                   asset_path=None,
                   **kwargs):

        """
        Load custom |EMOD_s| files when creating :class:`EMODTask`.

        Args:
            asset_path: If an asset path is passed, the climate, dlls, and migrations will be searched there
            eradication_path: The eradication.exe path.
            config_path: The custom configuration file.
            campaign_path: The custom campaign file.
            demographics_paths: The custom demographics files (single file or a list).
            custom_reports_path: Custom reports file

        Returns: An initialized experiment
        """
        # Create the experiment
        task = cls(eradication_path=eradication_path, **kwargs)

        if ep4_path is not None:
            # Load dtk_*_process.py to COMPS Assets/python folder
            task = add_ep4_from_path(task, ep4_path)
        else:
            task.use_embedded_python = False

        return task

    def pre_creation(self, parent: Union[Simulation, IWorkflowItem], platform: 'IPlatform'):
        """
        Call before a task is executed. This ensures our configuration is properly done

        """

        # Gather the custom coordinator, individual, and node events
        self.set_command_line()
        super().pre_creation(parent, platform)
        if not platform.is_windows_platform():
            # print( "Target is LINUX!" )
            self.is_linux = True

    def set_command_line(self) -> NoReturn:
        """
        Build and set the command line object.

        Returns:

        """
        # In COMPS, it's rare to have to specify multiple paths because 'we' control the environment and
        # can put everything in Assets. The multiple input paths is useful for local command-line usage where
        # the input files are spread across different locations. Note that with symlinks it's trivial to put
        # all the files in one path without copying. The only exception here is when we are using dtk_pre_process
        # to create a (demographics) input file and this can not be in Assets.
        # input_path = "./Assets" # this works on windows

        # Both "./Assets\;." and "./Assets\\;." work but the former confuses the linter because it is expecting
        # a known escape code, e.g. "\n" - escaping the backslash with "\\" escapes the escape code (got that?).
        input_path = "./Assets\\;."

        # Create the command line according to self. location of the model
        if self.use_singularity:
            self.command = CommandLine("singularity", "exec", f"Assets/{self.sif_filename}", f"Assets/{self.executable_name}", "--config", f"{self.config_file_name}", "--dll-path", "./Assets")
        else:
            self.command = CommandLine(f"Assets/{self.executable_name}", "--config", f"{self.config_file_name}", "--dll-path", "./Assets")
        if self.use_embedded_python:    # This should be the always-use case but we're not quite there yet.
            self.command._options.update({"--python-script-path": "./Assets/python"})

        # We do this here because CommandLine tries to be smart and quote input_path, but it isn't quite right...
        self.command.add_raw_argument("--input-path")
        self.command.add_raw_argument(input_path)

    def set_sif(self, path_to_sif) -> NoReturn:
        """
        Set the Singularity Image File.

        Returns:

        """
        # check if file is a SIF or an ID.
        if path_to_sif.endswith(".id"):
            ac = AssetCollection.from_id_file(path_to_sif)
            self.common_assets.add_assets(ac)
            self.sif_filename = [acf.filename for acf in ac.assets if acf.filename.endswith('.sif')][0]
        else:
            self.common_assets.add_asset(path_to_sif)
            self.sif_filename = pathlib.Path(path_to_sif).name
        self.use_singularity = True

    def gather_common_assets(self) -> AssetCollection:
        """
        Gather Experiment Level Assets
        Returns:

        """
        return self.common_assets

    def gather_transient_assets(self) -> AssetCollection:
        """
        Gather assets that are per simulation
        Returns:

        """

        # This config code needs to be rewritten
        # task.config contains emod-api version of config i.e., with schema. Needs to be finalized and written.
        if logger.isEnabledFor(DEBUG):
            logger.debug("DEBUG: Calling finalize.")

        return self.transient_assets



