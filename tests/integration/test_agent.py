# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from app.agent import root_agent


def test_agent_structure() -> None:
    """Integration test verifying agent root structure and tool registrations."""
    assert root_agent.name == "financial_coordinator"
    assert len(root_agent.sub_agents) == 3
    tool_names = [t.name if hasattr(t, "name") else str(t) for t in root_agent.tools]
    assert "fetch_realtime_stock_quote" in tool_names or any("stock_quote" in t for t in tool_names)
