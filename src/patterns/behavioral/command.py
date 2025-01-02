"""
@startuml
title classDiagram: Command Pattern
    class WebDriverUtils {
        +add_random_delay()
        +debug_page_state(driver)
        +wait_for_element_clickable(driver, xpath, timeout)
        +safe_click(driver, element)
    }
    class SystemUtils {
        +check_system_health(config)
    }
    class Config {
        +paths
        -download_dir
        -screenshot_dir
    }
    class WebDriver {
        +current_url
        +title
        +find_elements()
        +execute_script()
    }
    WebDriverUtils ..> WebDriver : uses
    SystemUtils ..> Config : uses
    SystemUtils ..> WebDriver : checks
@enduml
"""
"""
@startuml
title sequenceDiagram
    participant ClientCode as "Client Code"
    participant Logger as "setup_logging()"
    participant FileSystem as "File System"
    participant LogConfig as "logging.basicConfig"

    ClientCode->>Logger: setup_logging(log_dir)

    alt log_dir not provided
        Logger->>Logger: Set log_dir to cwd
    end

    Logger->>FileSystem: mkdir(log_dir)
    Logger->>Logger: Generate timestamp
    Logger->>Logger: Create log_file path

    Logger->>LogConfig: Configure logging
    activate LogConfig
    LogConfig->>FileSystem: Create FileHandler
    LogConfig->>LogConfig: Create StreamHandler
    LogConfig->>LogConfig: Set format & level
    deactivate LogConfig

    Logger-->>ClientCode: Return log_file path
@enduml
"""

import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
import logging

class WebDriverUtils:
    @staticmethod
    def add_random_delay(min_seconds=1, max_seconds=3):
        time.sleep(random.uniform(min_seconds, max_seconds))

    @staticmethod
    def debug_page_state(driver):
        logging.debug(f"Current URL: {driver.current_url}")
        logging.debug(f"Page Title: {driver.title}")
        logging.debug(f"Page Source Length: {len(driver.page_source)}")

    @staticmethod
    def wait_for_element_clickable(driver, xpath, timeout=10):
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    @staticmethod
    def safe_click(driver, element):
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        WebDriverUtils.add_random_delay(0.5, 1.5)
        element.click()

class Config:
    def __init__(self, base_dir: Path):
        self.paths = {
            'download': base_dir / 'downloads',
            'screenshot': base_dir / 'screenshots'
        }
        self._ensure_dirs_exist()

    def _ensure_dirs_exist(self):
        for path in self.paths.values():
            path.mkdir(parents=True, exist_ok=True)

class SystemUtils:
    @staticmethod
    def check_system_health(config: Config):
        checks = {
            'dirs_accessible': all(path.exists() for path in config.paths.values()),
            'webdriver_responsive': None  # Implement actual check
        }
        return all(checks.values()), checks