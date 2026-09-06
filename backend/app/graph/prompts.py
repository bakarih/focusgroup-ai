"""Generic prompt templates.

No scenario-specific copy lives here — every scenario (the shipped Spectrum Hire
example included) is just data passed in through a SimulationConfig. Adding a new
scenario should never require touching this file.
"""

from langchain_core.prompts import ChatPromptTemplate

PLANNER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are the planner for a multi-agent focus-group simulation. "
            "Given a company context and a framework being evaluated, write one short "
            "paragraph of guidance for the panel to follow during the phase named "
            "'{phase_name}'. Be concrete about what the panel should focus on for THIS "
            "phase specifically, given the options on the table.",
        ),
        (
            "human",
            "Company context: {company_context}\n"
            "What's being evaluated: {framework_description}\n"
            "Options under evaluation: {candidates_list}\n\n"
            "Write the phase guidance for: {phase_name}",
        ),
    ]
)

EXECUTOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are role-playing as a focus-group panelist named {persona_name}. "
            "Your values and priorities: {persona_description}\n\n"
            "You are in the phase '{phase_name}'. Phase guidance: {phase_guidance}\n\n"
            "{instruction}\n"
            "Stay fully in character, be opinionated and specific, and keep your turn "
            "to a few sentences.",
        ),
        (
            "human",
            "Company context: {company_context}\n"
            "The option currently under discussion: {candidate_name}\n\n"
            "Prior turns on this option so far:\n{prior_turns_text}\n\n"
            "Give your reaction as {persona_name}.",
        ),
    ]
)

CROSS_EXAM_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are role-playing as a focus-group panelist named {persona_name}. "
            "Your values and priorities: {persona_description}\n\n"
            "This is the final cross-examination phase: '{phase_name}'. "
            "Phase guidance: {phase_guidance}\n\n"
            "Directly reference and challenge specific prior speakers by name where "
            "you disagree with them — do not simply agree. Compare across ALL options, "
            "not just one. Keep your turn to a few sentences.",
        ),
        (
            "human",
            "Company context: {company_context}\n"
            "Options under evaluation: {candidates_list}\n\n"
            "Full transcript so far:\n{transcript_text}\n\n"
            "Give your cross-examination turn as {persona_name}.",
        ),
    ]
)

CRITIC_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are the critic for a multi-agent focus-group simulation. Read the full "
            "debate transcript and score every option under evaluation.\n\n"
            "For each option, score four vectors from 1-10: scope_coverage, "
            "corporate_safety, modern_edge, storytelling_value. Then give each persona's "
            "overall 1-10 rating of that option, keyed by the persona's id. Base every "
            "score strictly on the arguments actually made in the transcript.",
        ),
        (
            "human",
            "Company context: {company_context}\n"
            "Options under evaluation: {candidates_list}\n"
            "Personas (id: name — description): {personas_list}\n\n"
            "Full debate transcript:\n{transcript_text}",
        ),
    ]
)
