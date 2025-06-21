import os
from typing import Optional


def get_sequence_from_env(env_name: str) -> set[int]:
    """
    Retrieve a set of integers from an environment variable.

    The environment variable is expected to contain a semicolon-separated string of integers.
    For example: "123;456;789" will be converted to the set {123, 456, 789}.

    Args:
        env_name: The name of the environment variable to retrieve.

    Returns:
        A set of integers parsed from the environment variable.

    Raises:
        EnvironmentError: If the environment variable is not set or is empty.
        ValueError: If any of the values in the environment variable cannot be converted to int.
    """
    values = os.getenv(env_name)
    if not values:
        raise EnvironmentError(f"Env {env_name} isn't specified in OS Environment")
    return set([int(value) for value in values.split(";")])


def get_env_var(
    env_name: str, default: Optional[str] = None, raise_exc: bool = False
) -> str:
    """
    Retrieve a required environment variable or return the provided default.

    This function attempts to fetch the value of the specified environment
    variable. If it is not found and a default is provided, the default is returned.
    Otherwise, an exception is raised.

    Args:
        env_name (str): The name of the environment variable to retrieve.
        default (Optional[str]): A fallback value to use if the variable is not set.

    Returns:
        str: The value of the environment variable or the default value.

    Raises:
        EnvironmentError: If the environment variable is not set and no default is provided.
    """
    value = os.getenv(env_name)
    if value is not None:
        return value
    if default is not None:
        return default
    if raise_exc:
        raise EnvironmentError(f"Env {env_name} isn't specified in OS Environment")

    raise EnvironmentError(
        f"Env {env_name} not found and no default provided (raise_exc=False)"
    )
