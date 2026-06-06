from dataclasses import dataclass

from app.utils.prompt_utils import optimize_prompt


@dataclass(slots=True)
class PromptOptimizationResult:
    """Optimized prompt payload used by the ask workflow."""

    original_prompt: str
    optimized_prompt: str


class PromptOptimizerService:
    """Apply conservative prompt optimizations with fail-open behavior."""

    def optimize(self, prompt: str) -> PromptOptimizationResult:
        """Return an optimized prompt, falling back to the original on failure."""

        try:
            optimized_prompt = optimize_prompt(prompt)
        except Exception:
            optimized_prompt = prompt

        if not optimized_prompt.strip():
            optimized_prompt = prompt

        return PromptOptimizationResult(original_prompt=prompt, optimized_prompt=optimized_prompt)