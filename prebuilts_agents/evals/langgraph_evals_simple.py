import json
from agentevals.trajectory.match import create_trajectory_match_evaluator

outputs = [
    {
        "role": "assistant",
        "tool_calls": [
            {
                "function": {
                    "name": "get_weather",
                    "arguments": json.dumps({"city": "san francisco"}),
                }
            },
            {
                "function": {
                    "name": "get_directions",
                    "arguments": json.dumps({"destination": "presidio"}),
                }
            }
        ],
    }
]
reference_outputs = [
    {
        "role": "assistant",
        "tool_calls": [
            {
                "function": {
                    "name": "get_weather",
                    "arguments": json.dumps({"city": "san francisco"}),
                }
            },
        ],
    }
]

# Create the evaluator
evaluator = create_trajectory_match_evaluator(
    trajectory_match_mode="superset",
)

# Run the evaluator
result = evaluator(
    outputs=outputs, reference_outputs=reference_outputs
)
print(result)