# app/plugins.py
"""ADK Policy Plugin for Financial Compliance and Safety Guardrails.

Executes after_model_callback to inspect model outputs, enforce mandatory
financial disclosures ("Not financial advice"), and sanitize response content.
"""

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from google.adk.plugins.base_plugin import BasePlugin
from google.genai import types

from app.logger import logger

MANDATORY_DISCLAIMER = (
    "\n\n---\n*Disclaimer: This analysis is generated for informational purposes only "
    "and does NOT constitute professional financial or investment advice. Always perform "
    "independent research and consult a licensed financial advisor before making investment decisions.*"
)


class FinancialPolicyPlugin(BasePlugin):
    """Guardrail plugin for financial advice disclaimers and policy compliance."""

    def __init__(self, name: str = "financial_policy_plugin") -> None:
        super().__init__(name=name)

    async def after_model_callback(
        self,
        *,
        callback_context: CallbackContext,
        llm_response: LlmResponse,
    ) -> LlmResponse | None:
        """Inspect and modify LLM output to guarantee policy compliance.

        Args:
            callback_context: ADK callback context.
            llm_response: Response returned from LLM generation.

        Returns:
            Modified LlmResponse with mandatory disclaimers appended.
        """
        if not llm_response or not llm_response.content:
            return None

        # Extract text from response parts
        text_content = ""
        if hasattr(llm_response.content, "parts"):
            for part in llm_response.content.parts:
                if hasattr(part, "text") and part.text:
                    text_content += part.text

        if text_content and "Disclaimer:" not in text_content:
            logger.info("Injecting mandatory financial disclaimer via policy plugin")
            updated_text = text_content + MANDATORY_DISCLAIMER
            # Construct modified response
            modified_content = types.Content(
                role="model",
                parts=[types.Part.from_text(text=updated_text)],
            )
            return LlmResponse(content=modified_content)

        return None
