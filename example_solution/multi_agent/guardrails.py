from agents import (
    Agent,
    GuardrailFunctionOutput,
    MessageOutputItem,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
)
from pydantic import BaseModel


class BaseGuardrail(BaseModel):
    should_trip: bool
    reasoning: str


class RelevanceOutput(BaseGuardrail):
    pass


class JailbreakOutput(BaseGuardrail):
    pass


class SensitiveOutput(BaseGuardrail):
    pass


class GuardrailAgent(Agent):
    output_type: type[BaseGuardrail]


def get_guardrail_message(
    guardrail_name: str,
    guardrail_output: BaseGuardrail,
) -> str:
    """
    Returns a formatted string for the guardrail output.
    """
    return (
        f"{guardrail_name} {'tripped' if guardrail_output.should_trip else 'passed'}"
        f"\nReasoning: {guardrail_output.reasoning}"
    )


def make_input_guardrail(
    guardrail_agent: GuardrailAgent,
):
    """
    Creates an input guardrail for the given guardrail agent.
    """
    guardrail_name = f"{guardrail_agent.name}_input_guardrail"

    @input_guardrail
    async def guardrail(
        ctx: RunContextWrapper[None],
        agent: Agent,
        input: str | list[TResponseInputItem],
    ) -> GuardrailFunctionOutput:
        result = await Runner.run(guardrail_agent, input, context=ctx.context)
        final_output: BaseGuardrail = result.final_output_as(agent.output_type)

        output_info = get_guardrail_message(guardrail_name, final_output)
        return GuardrailFunctionOutput(
            output_info=output_info,
            tripwire_triggered=final_output.should_trip,
        )

    guardrail.__name__ = guardrail_name
    return guardrail


def make_output_guardrail(
    guardrail_agent: GuardrailAgent,
):
    """
    Creates an output guardrail for the given guardrail agent.
    """
    guardrail_name = f"{guardrail_agent.name}_output_guardrail"

    @output_guardrail
    async def guardrail(
        ctx: RunContextWrapper[None],
        agent: Agent,
        output: MessageOutputItem,
    ) -> GuardrailFunctionOutput:
        result = await Runner.run(guardrail_agent, output, context=ctx.context)
        final_output: BaseGuardrail = result.final_output_as(agent.output_type)

        output_info = get_guardrail_message(guardrail_name, final_output)
        return GuardrailFunctionOutput(
            output_info=output_info,
            tripwire_triggered=final_output.should_trip,
        )

    guardrail.__name__ = guardrail_name
    return guardrail
