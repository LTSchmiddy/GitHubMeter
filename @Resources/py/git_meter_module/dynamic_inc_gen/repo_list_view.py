import os, pathlib

from configparser import ConfigParser

def generate_repo_list_meters(
    subpath: str, 
    repo_count: int = 5, 
    # offsetX: int = 0,
    # offsetY: int = 40,
    # spacingV: int = 20, 
    # entryW: int = 350,
    # entryH: int = 30,
):
    cfg: ConfigParser = ConfigParser()
    
    def buildPosX(var: str):
        return f"(#offsetX# + #{var}#)"
    
    def buildPosY(var: str, index: int):
        return f"(#offsetY# + #entryH# * {index} + #spacingV# * {index} + #{var}#)"
    
    def generate_repo_slot(cfg: ConfigParser, index: int) -> dict:
        cfg[f"meterRepoName{index}"] = {
            "DynamicVariables": 1,
            "Meter": "String",
            "MeterStyle": "#RepoNameStyle#",
            "MeasureName": "#RepoMeasure#",
            "W": "#entryNameW#",
            "H": "#entryNameH#",
            "X": buildPosX("entryNameX"),
            "Y": buildPosY("entryNameY", i),
            "Text": f"[#RepoMeasure#:Func(RepoName, {index})]",    
        }
        
        cfg[f"meterRepoDate{index}"] = {
            "DynamicVariables": 1,
            "Meter": "String",
            "MeterStyle": "#RepoDateStyle#",
            "MeasureName": "#RepoMeasure#",
            "W": "#entryDateW#",
            "H": "#entryDateH#",
            "X": buildPosX("entryDateX"),
            "Y": buildPosY("entryDateY", i),
            "Text": f"[#RepoMeasure#:Func(RepoUpdatedAt, {index})]",    
        }

        cfg[f"meterRepoCommitMessage{index}"] = {
            "DynamicVariables": 1,
            "Meter": "String",
            "MeterStyle": "#RepoLCMStyle#",
            "MeasureName": "#RepoMeasure#",
            "W": "#entryCommitMessageW#",
            "H": "#entryCommitMessageH#",
            "X": buildPosX("entryCommitMessageX"),
            "Y": buildPosY("entryCommitMessageY", i),
            "Text": f"[#RepoMeasure#:Func(RepoLastCommitMessage, {index})]",    
        }
        
        cfg[f"meterRepoCommitAuthor{index}"] = {
            "DynamicVariables": 1,
            "Meter": "String",
            "MeterStyle": "#RepoLCAStyle#",
            "MeasureName": "#RepoMeasure#",
            "W": "#entryCommitAuthorW#",
            "H": "#entryCommitAuthorH#",
            "X": buildPosX("entryCommitAuthorX"),
            "Y": buildPosY("entryCommitAuthorY", i),
            "Text": f"By [#RepoMeasure#:Func(RepoLastCommitAuthor, {index})]",    
        }
    
    
    
    
    for i in range (0, repo_count):
        generate_repo_slot(cfg, i)
        
    cfg_file = open(pathlib.Path("dynamic_inc").joinpath(subpath+".inc"), 'w')
    cfg.write(cfg_file)
    cfg_file.close()

if __name__ == '__main__':
    generate_repo_list_meters("repo_list_view")