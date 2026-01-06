"""
LLM utilities for generating realistic text content.

This module provides optional integration with an LLM (Claude)
to generate realistic task names, descriptions, and comments.
If no API key is provided, the pipeline safely falls back to
template-based generation.
"""

import json
import time
from typing import Optional, Union

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

from src.config import (
    ANTHROPIC_API_KEY,
    USE_LLM_GENERATION,
    LLM_MODEL,
    LLM_MAX_TOKENS,
    LLM_TEMPERATURE
)

# -----------------------------------------------------------------------------
# CLIENT INITIALIZATION
# -----------------------------------------------------------------------------

client = None

if USE_LLM_GENERATION and Anthropic is not None:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)


# -----------------------------------------------------------------------------
# CORE GENERATION FUNCTION
# -----------------------------------------------------------------------------

def generate_with_llm(
    prompt: str,
    expect_json: bool = False,
    retries: int = 3,
    retry_delay: float = 1.5
) -> Optional[Union[str, dict]]:
    """
    Generate text using Claude LLM.

    Args:
        prompt (str): Prompt sent to the LLM.
        expect_json (bool): Whether output should be parsed as JSON.
        retries (int): Number of retry attempts on failure.
        retry_delay (float): Delay between retries in seconds.

    Returns:
        str | dict | None:
            - Generated text
            - Parsed JSON (if expect_json=True)
            - None if LLM generation is disabled or fails
    """

    if not USE_LLM_GENERATION or client is None:
        return None

    for attempt in range(retries):
        try:
            response = client.messages.create(
                model=LLM_MODEL,
                max_tokens=LLM_MAX_TOKENS,
                temperature=LLM_TEMPERATURE,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            text = response.content[0].text.strip()

            if expect_json:
                text = _clean_json_response(text)
                return json.loads(text)

            return text

        except Exception as e:
            if attempt == retries - 1:
                print(f"[LLM ERROR] Failed after {retries} attempts: {e}")
                return None
            time.sleep(retry_delay)

    return None


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def _clean_json_response(text: str) -> str:
    """
    Clean JSON output from LLM by removing markdown fences.

    Args:
        text (str): Raw LLM output

    Returns:
        str: Clean JSON string
    """
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


# -----------------------------------------------------------------------------
# HIGH-LEVEL CONTENT HELPERS (OPTIONAL)
# -----------------------------------------------------------------------------

def generate_task_name(prompt: str) -> Optional[str]:
    """
    Generate a task name using LLM.

    Returns None if LLM is disabled.
    """
    return generate_with_llm(prompt)


def generate_task_description(prompt: str) -> Optional[str]:
    """
    Generate a task description using LLM.

    Returns None if LLM is disabled.
    """
    return generate_with_llm(prompt)


def generate_comment(prompt: str) -> Optional[str]:
    """
    Generate a task comment using LLM.

    Returns None if LLM is disabled.
    """
    return generate_with_llm(prompt)
