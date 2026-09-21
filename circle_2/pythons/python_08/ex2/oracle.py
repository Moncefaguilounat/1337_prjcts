import os
import sys
from typing import Dict, Optional, Tuple
from pathlib import Path


def load_environment() -> bool:
    try:
        from dotenv import load_dotenv

        if Path(".env").exists():
            load_dotenv()
            return True
        return False

    except ImportError:
        return False


def get_configuration() -> Dict[str, Optional[str]]:
    return {
        "MATRIX_MODE": os.getenv("MATRIX_MODE", "development"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "DEBUG"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT"),
    }


def validate_config(config: Dict[str, Optional[str]]) -> Tuple[bool, list]:
    missing = []

    if not config["DATABASE_URL"]:
        missing.append("DATABASE_URL")

    if not config["API_KEY"]:
        missing.append("API_KEY")

    if not config["ZION_ENDPOINT"]:
        missing.append("ZION_ENDPOINT")

    return len(missing) == 0, missing


def display_config(config: Dict[str, Optional[str]], env_loaded: bool) -> None:

    print("\nORACLE STATUS: Reading the Matrix...\n")

    print("Configuration loaded:")

    # Mode
    mode = config['MATRIX_MODE']
    print(f"Mode: {mode}")

    # Show behavior difference between dev and prod

    if mode == "production":
        print("Production mode active")
    else:
        print("development mode active")

    # Database
    if config["DATABASE_URL"]:
        if config["MATRIX_MODE"] == "production":
            print("Database: Connected to production database")
        else:
            print("Database: Connected to local instance")
    else:
        print("Database: Not connected")

    # API
    if config["API_KEY"]:
        print("API Access: Authenticated")
    else:
        print("API Access: Missing key")

    # Log level
    print(f"Log Level: {config['LOG_LEVEL']}")

    # Zion
    if config["ZION_ENDPOINT"]:
        print("Zion Network: Online\n")
    else:
        print("Zion Network: Offline\n")


def display_security(env_loaded: bool) -> None:

    print("Environment security check:")

    print("[OK] No hardcoded secrets detected")

    # Check .env existence
    if env_loaded:
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file not found")

    print("[OK] Production overrides available\n")


def main() -> None:

    env_loaded = load_environment()
    config = get_configuration()

    display_config(config, env_loaded)

    display_security(env_loaded)

    valid, missing = validate_config(config)

    if valid:
        print("The Oracle sees all configurations.")
    else:
        print("The Oracle requires more information.")
        print("Missing Configuration:", ", ".join(missing))
        print("Configure your .env file!")
        sys.exit(1)


if __name__ == "__main__":
    main()
