"""
Learning Companion Agent - Helps students understand notebook concepts through:
1. Concept Explanation - Identifies and explains key learning objectives
2. Code Modification Suggestions - Proposes experiments to deepen understanding
"""

import json
from openai import OpenAI
from typing import Dict, List, Any

class LearningAgent:
    def __init__(self):
        self.openai = OpenAI()
        self.model = "gpt-4o"

    def parse_notebook(self, notebook_path: str) -> List[Dict[str, Any]]:
        """Parse a Jupyter notebook and extract cells with their content."""
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)

        cells = []
        for idx, cell in enumerate(notebook['cells']):
            cell_data = {
                'index': idx,
                'type': cell['cell_type'],
                'source': ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source'],
                'id': cell.get('id', f'cell-{idx}')
            }
            cells.append(cell_data)

        return cells

    def explain_concept(self, cell_content: str, cell_index: int, context_cells: List[Dict] = None) -> str:
        """
        Analyzes a code cell and explains:
        - What the code does
        - Why it's important
        - What concepts it demonstrates
        - How it connects to previous cells
        """

        # Build context from previous cells
        context = ""
        if context_cells:
            context = "Previous cells executed:\n"
            for cell in context_cells[-3:]:  # Last 3 cells for context
                if cell['type'] == 'code':
                    context += f"Cell {cell['index']}: {cell['source'][:100]}...\n"

        prompt = f"""You are a patient, expert programming tutor helping a student understand Jupyter notebook code.

{context}

Current cell (Cell {cell_index}):
```python
{cell_content}
```

Please explain this cell by covering:
1. **What it does**: A clear, simple explanation of what this code accomplishes
2. **Key concepts**: The important programming or AI concepts being demonstrated
3. **Why it matters**: How this fits into the bigger picture of learning about AI agents
4. **Connection**: How this builds on or relates to previous cells

Keep your explanation clear, concise, and encouraging. Use analogies when helpful.
Format your response in markdown.
"""

        messages = [{"role": "user", "content": prompt}]
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return response.choices[0].message.content

    def suggest_experiments(self, cell_content: str, cell_index: int) -> str:
        """
        Suggests code modifications and experiments to help students:
        - Understand what different parts do
        - See cause and effect
        - Learn through hands-on experimentation
        """

        prompt = f"""You are a creative programming tutor who believes students learn best by experimenting.

Here's a code cell from a Jupyter notebook:

```python
{cell_content}
```

Please suggest 3-5 specific experiments the student can try to deepen their understanding. For each experiment:
1. Describe what to modify in the code
2. Predict what will happen
3. Explain what concept this experiment demonstrates

Make the experiments progressively more challenging:
- Start with simple modifications (change a value, remove a parameter)
- Progress to more complex changes (restructure code, add features)

Format each experiment like this:

### Experiment N: [Catchy title]
**What to do:** [Specific code change]
**Prediction:** [What will happen]
**Why it matters:** [What concept this teaches]
**Code snippet:**
```python
[Modified code]
```

Be specific with code examples. Format your response in markdown.
"""

        messages = [{"role": "user", "content": prompt}]
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return response.choices[0].message.content

    def analyze_cell(self, notebook_path: str, cell_index: int) -> Dict[str, str]:
        """
        Complete analysis of a specific cell combining concept explanation
        and experimental suggestions.
        """
        cells = self.parse_notebook(notebook_path)

        if cell_index >= len(cells):
            return {"error": f"Cell index {cell_index} out of range. Notebook has {len(cells)} cells."}

        target_cell = cells[cell_index]

        if target_cell['type'] != 'code':
            return {"info": f"Cell {cell_index} is a markdown cell, not code."}

        # Get context from previous cells
        context_cells = cells[:cell_index] if cell_index > 0 else []

        # Generate both analyses
        explanation = self.explain_concept(
            target_cell['source'],
            cell_index,
            context_cells
        )

        experiments = self.suggest_experiments(
            target_cell['source'],
            cell_index
        )

        return {
            'cell_index': cell_index,
            'cell_content': target_cell['source'],
            'explanation': explanation,
            'experiments': experiments
        }

    def interactive_session(self, notebook_path: str, cell_index: int):
        """
        Runs an interactive learning session for a specific cell.
        """
        print(f"\n{'='*80}")
        print(f"  Learning Companion - Analyzing Cell {cell_index}")
        print(f"{'='*80}\n")

        result = self.analyze_cell(notebook_path, cell_index)

        if 'error' in result or 'info' in result:
            print(result.get('error') or result.get('info'))
            return

        print(f"📚 CELL CODE:\n")
        print("```python")
        print(result['cell_content'])
        print("```\n")

        print(f"{'─'*80}")
        print("\n🎓 CONCEPT EXPLANATION\n")
        print(result['explanation'])

        print(f"\n{'─'*80}")
        print("\n🔬 HANDS-ON EXPERIMENTS\n")
        print(result['experiments'])

        print(f"\n{'='*80}\n")


# Example usage
if __name__ == "__main__":
    import sys

    # Default to analyzing lab1
    notebook_path = "1_lab1.ipynb"
    cell_index = 10  # The OpenAI() initialization cell

    # Allow command line arguments
    if len(sys.argv) > 1:
        cell_index = int(sys.argv[1])
    if len(sys.argv) > 2:
        notebook_path = sys.argv[2]

    agent = LearningAgent()
    agent.interactive_session(notebook_path, cell_index)
