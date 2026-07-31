import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
from datetime import datetime
import yaml
import re
import csv


# ======================================
# 1. 路径配置
# ======================================

CSV_PATH = Path("../data/arper_collection.csv")

YAML_PATH = Path(
    "../config/arper_selectors_simple.yaml"
)

OUTPUT_DIR = Path("../outputs")



# ======================================
# 2. 读取 YAML 配置
# ======================================

def load_selector_config():

    with open(
        YAML_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return yaml.safe_load(f)
