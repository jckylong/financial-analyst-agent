# app/memory.py
"""ADK Memory Bank Integration and Async Memory Consolidation.

Provides persistent cross-session memory tools and non-blocking background
task execution for memory generation.
"""

import asyncio

from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import preload_memory

from app.logger import logger

_background_tasks = set()


async def generate_memories_callback(callback_context: CallbackContext) -> None:
    """Consolidate conversation events into long-term Memory Bank asynchronously.

    Runs as a background task to prevent UI latency and non-blocking operation.

    Args:
        callback_context: ADK callback context containing session events.
    """
    async def _async_memory_task() -> None:
        try:
            logger.info("Starting background memory consolidation task")
            await callback_context.add_session_to_memory()
            logger.info("Completed background memory consolidation task")
        except Exception as err:
            logger.warning("Async memory consolidation encountered warning", error=str(err))

    # Fire-and-forget background task with stored reference
    task = asyncio.create_task(_async_memory_task())
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    return None


def get_preload_memory_tool():
    """Returns ADK preload_memory tool instance for injecting long-term memories.

    Returns:
        preload_memory tool object configured for memory retrieval.
    """
    return preload_memory
