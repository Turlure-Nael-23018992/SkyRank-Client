import os, sys, sqlite3, time
from pathlib import Path
from typing import List

# Patch sys.path to allow internal imports from SkyRank
SKYRANK_PATH = os.path.join(os.path.dirname(__file__), '..', 'SkyRank')
sys.path.insert(0, os.path.abspath(SKYRANK_PATH))

# Add external dependencies (Bbs and RTree)
EXTERNAL_PATH = os.path.join(os.path.dirname(__file__), '..', 'external', 'BBS')
sys.path.append(os.path.join(EXTERNAL_PATH, 'Bbs'))
sys.path.append(os.path.join(EXTERNAL_PATH, 'RTree'))

# Force working directory to the project root (SkyRank-Client/)
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Patch DataConverter to use absolute path for TestExecution.db
from SkyRank.Utils.DataModifier.DataConverter import DataConverter
from SkyRank.Utils.DataModifier.DictToDatabase import DictToDatabase

original_init = DataConverter.__init__

def patched_init(self, data):
    if isinstance(data, dict) or (isinstance(data, str) and data.endswith('.json')):
        abs_db_path = os.path.abspath("SkyRank/Assets/AlgoExecution/DbFiles/TestExecution.db")
        self.data = data
        self.DictToDatabase = DictToDatabase(abs_db_path)
    else:
        self.data = data
        self.DictToDatabase = None

DataConverter.__init__ = patched_init

# Internal SkyRank imports
from SkyRank.Algorithms.CoskySql import CoskySQL
from SkyRank.Algorithms.CoskyAlgorithme import CoskyAlgorithme
from SkyRank.Algorithms.DpIdpDh import DpIdpDh
from SkyRank.Algorithms.RankSky import RankSky
from SkyRank.Algorithms.SkyIR import SkyIR

from SkyRank.Utils.Preference import Preference
from SkyRank.Utils.DataModifier.DataConverter import DataConverter
from SkyRank.Utils.DataTypes.JsonObject import JsonObject
from SkyRank.Utils.DataTypes.DbObject import DbObject
from SkyRank.Utils.DataTypes.DictObject import DictObject
from SkyRank.Utils.DisplayHelpers import print_red
from SkyRank.Database.DatabaseHelpers import Database


class SkyRankEngine:
    """
    SkyRankEngine: a client-facing class to run algorithms without export.

    This class mimics the internal App.py behavior but only requires data objects
    (DictObject, JsonObject, or DbObject) and algorithm references.
    """

    def __init__(self, data, algo, preferences):
        self.algo_instance = None
        self.pref = preferences
        self.results = None

        # Detect input data type
        if isinstance(data, DictObject):
            self.r, self.dataName = data.r, "DictObject"
            nb_cols = len(next(iter(self.r.values())))
        elif isinstance(data, JsonObject):
            self.jsonFp, self.dataName = data.fp, "JsonObject"
            import json
            rel = json.loads(Path(self.jsonFp).read_text(encoding="utf-8"))
            nb_cols = len(next(iter(rel.values())))
        elif isinstance(data, DbObject):
            self.dbFp, self.dataName = data.fp, "DbObject"
            print("self.dbFp", self.dbFp)
            nb_cols = self._count_db_columns(self.dbFp) - 1
            print(f"Column count: {nb_cols}")
        else:
            raise ValueError("Unsupported DataObject")

        # Validate preferences for applicable algorithms
        if algo.__name__ in {"RankSky", "CoskyAlgorithme", "CoskySQL"}:
            if self.pref is None or len(self.pref) != nb_cols:
                raise ValueError("Preference list must match column count.")

        self.algo = algo.__name__

        # Dispatch execution
        start = time.perf_counter()
        self._dispatch()

    def _dispatch(self):
        match self.algo:
            case "CoskyAlgorithme":
                self._start_cosky_algorithme()
            case "CoskySQL":
                self._start_cosky_sql()
            case "DpIdpDh":
                self._start_dp_idp_dh()
            case "RankSky":
                self._start_ranksky()
            case "SkyIR":
                self._start_skyir()
            case _:
                raise ValueError("Unknown algorithm")

    def _start_cosky_sql(self):
        print_red("Starting CoskySQL")
        if self.dataName == "DbObject":
            self.algo_instance = CoskySQL(self.dbFp, self.pref)
        elif self.dataName == "JsonObject":
            DataConverter(self.jsonFp).jsonToDb()
            self.algo_instance = CoskySQL(
                "SkyRank/Assets/AlgoExecution/DbFiles/TestExecution.db", self.pref
            )
        else:
            DataConverter(self.r).relationToDb()
            self.algo_instance = CoskySQL(
                "SkyRank/Assets/AlgoExecution/DbFiles/TestExecution.db", self.pref
            )
        self.results = self.algo_instance.rows_res

    def _start_cosky_algorithme(self):
        print_red("Starting CoskyAlgorithme")
        if self.dataName == "DbObject":
            rel = DataConverter(self.dbFp).dbToRelation()
            self.algo_instance = CoskyAlgorithme(rel, self.pref)
        elif self.dataName == "JsonObject":
            rel = DataConverter(self.jsonFp).jsonToRelation()
            self.algo_instance = CoskyAlgorithme(rel, self.pref)
        else:
            self.r = {k: tuple(v) for k, v in self.r.items()}
            self.algo_instance = CoskyAlgorithme(self.r, self.pref)
        self.results = self.algo_instance.s

    def _start_dp_idp_dh(self):
        print_red("Starting DpIdpDh")
        if self.dataName == "DbObject":
            rel = DataConverter(self.dbFp).dbToRelation()
            self.algo_instance = DpIdpDh(rel)
        elif self.dataName == "JsonObject":
            rel = DataConverter(self.jsonFp).jsonToRelation()
            self.algo_instance = DpIdpDh(rel)
        else:
            self.r = {k: tuple(v) for k, v in self.r.items()}
            self.algo_instance = DpIdpDh(self.r)
        self.results = self.algo_instance.


    def _start_ranksky(self):
        print_red("Starting RankSky")
        if self.dataName == "DbObject":
            print("in here")
            rel = DataConverter(self.dbFp)
            rel = rel.dbToRelation()
            self.algo_instance = RankSky(rel, self.pref)
        elif self.dataName == "JsonObject":
            rel = DataConverter(self.jsonFp).jsonToRelation()
            self.algo_instance = RankSky(rel, self.pref)
        else:
            self.r = {k: tuple(v) for k, v in self.r.items()}
            self.algo_instance = RankSky(self.r, self.pref)

    def _start_skyir(self):
        print_red("Starting SkyIR")
        if self.dataName == "DbObject":
            rel = DataConverter(self.dbFp).dbToRelation()
            self.algo_instance = SkyIR(rel)
        elif self.dataName == "JsonObject":
            rel = DataConverter(self.jsonFp).jsonToRelation()
            self.algo_instance = SkyIR(rel)
        else:
            self.r = {k: tuple(v) for k, v in self.r.items()}
            self.algo_instance = SkyIR(self.r)
        self.algo_instance.skyIR(10)

    @staticmethod
    def _count_db_columns(db_path: str) -> int:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("PRAGMA table_info(Pokemon)")
        n = len(cur.fetchall())
        con.close()
        return n


if __name__ == "__main__":
    """
    Example main usage
    -------------------
    This block demonstrates how to run a SkyRank algorithm using a JSON file as input.

    Supported input formats:
    - DictObject: pass a Python dictionary {id: (val1, val2, ...)}
    - JsonObject: pass the path to a JSON file with structure {"1": [v1, v2, ...], ...}
    - DbObject: pass the path to a SQLite database file containing a table named 'Pokemon'

    Algorithm choices:
    - CoskySQL
    - CoskyAlgorithme
    - RankSky
    - DpIdpDh
    - SkyIR

    How to use:
    -----------
    1. Define the input data (here: a JSON file path).
    2. Wrap it into a DataObject (JsonObject, DictObject, or DbObject).
    3. Define the algorithm to use.
    4. Define the preference list (only for Cosky*, RankSky).
    5. Instantiate SkyRankEngine with: SkyRankEngine(data_obj, algorithm, preferences).
    6. Access result through eng.algo_instance.

    To run this file:
        > python Client/Engine.py
    """

    # Example with JSON input
    json_path = "SkyRank/Assets/AlgoExecution/JsonFiles/RTuples8.json"  # Path to your input file

    # Define preferences: use Preference.MIN or Preference.MAX for each column

    prefs = [Preference.MIN, Preference.MIN, Preference.MIN] # Adjust as needed

    # Create the appropriate DataObject wrapper (can be JsonObject, DictObject, or DbObject)

    data_obj = JsonObject(json_path) # Change this to DictObject or DbObject as needed

    # Choose the algorithm to run (can also use CoskyAlgorithme, RankSky, etc.)

    algorithm = CoskySQL # Change this to the desired algorithm

    # Create the engine instance and run the algorithm
    eng = SkyRankEngine(data_obj, algorithm, preferences=prefs)

    # Access the internal result (depends on the algorithm structure)

