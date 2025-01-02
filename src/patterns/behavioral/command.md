```mermaid
classDiagram : 'Command Pattern'
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
```
