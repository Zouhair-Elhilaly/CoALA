
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Observation(BaseModel):
    """Represents an observation received by the agent."""

    id: UUID = Field(default_factory=uuid4)

    content: str = Field(min_length=1)

    source: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )


class RetrievedItem(BaseModel):
    """Represents information retrieved from a source."""

    id: UUID = Field(default_factory=uuid4)

    content: str = Field(min_length=1)

    source_id: str = Field(min_length=1)

    source_type: str | None = None

    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )


class WorkingMemory(BaseModel):
    """Temporary information actively used by the agent."""

    current_task: str | None = None

    current_goal: str | None = None

    observations: list[Observation] = Field(
        default_factory=list
    )

    retrieved_information: list[RetrievedItem] = Field(
        default_factory=list
    )

    intermediate_results: dict[str, Any] = Field(
        default_factory=dict
    )

    candidate_actions: list[str] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    def add_observation(
        self,
        content: str,
        source: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Observation:

        observation = Observation(
            content=content,
            source=source,
            metadata=metadata or {},
        )

        self.observations.append(observation)

        return observation

    def add_retrieved_item(
        self,
        content: str,
        source_id: str,
        source_type: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> RetrievedItem:

        item = RetrievedItem(
            content=content,
            source_id=source_id,
            source_type=source_type,
            metadata=metadata or {},
        )

        self.retrieved_information.append(item)

        return item

    def save_result(self, key: str, value: Any) -> None:

        if not key.strip():
            raise ValueError("Result key cannot be empty.")

        self.intermediate_results[key] = value

    def register_candidate_action(self, action_name: str) -> None:

        if not action_name.strip():
            raise ValueError("Action name cannot be empty.")

        if action_name not in self.candidate_actions:
            self.candidate_actions.append(action_name)
