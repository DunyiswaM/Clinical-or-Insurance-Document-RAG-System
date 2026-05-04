# Graphviz Rendering Guide

## View Graphviz Diagrams

After running this script, you'll have 4 Graphviz (.gv) files. Here's how to render them:

### Option 1: Online (Graphviz Online Editor)
1. Go to https://dreampuf.github.io/GraphvizOnline/
2. Copy-paste the contents of any .gv file
3. View the diagram instantly

### Option 2: Command Line (if Graphviz installed)

```bash
# Render to PNG
dot patient_journey.gv -Tpng -o patient_journey.png
dot condition_treatment.gv -Tpng -o condition_treatment.png
dot recovery_analysis.gv -Tpng -o recovery_analysis.png
dot cost_flow.gv -Tpng -o cost_flow.png

# Render to SVG (better for web)
dot patient_journey.gv -Tsvg -o patient_journey.svg
```

### Option 3: VS Code Plugin
- Install "Graphviz (dot) language support" extension
- Open .gv file -> Click "Preview" button

### Option 4: Python Script

```python
import subprocess

diagrams = ['patient_journey.gv', 'condition_treatment.gv', 
            'recovery_analysis.gv', 'cost_flow.gv']

for diagram in diagrams:
    output = diagram.replace('.gv', '.png')
    subprocess.run(['dot', '-Tpng', diagram, '-o', output])
    print(f"Generated {output}")
```

---

## Diagram Descriptions

### 1. patient_journey.gv
Shows the linear journey of a patient through the healthcare system:
- Patient Visit -> Diagnosis -> Treatment Selection -> Monitoring -> Recovery Assessment -> Complete

### 2. condition_treatment.gv  
Displays relationships between conditions and treatments:
- Shows patient counts per condition
- Average costs per treatment
- Treatment-condition associations

### 3. recovery_analysis.gv
Categorizes patients by recovery outcome:
- Low recovery (<40) -> Higher costs, more intervention needed
- Medium recovery (40-70) -> Standard care pathway
- High recovery (>70) -> Excellent outcomes, minimal follow-ups

### 4. cost_flow.gv
Traces cost drivers through decision points:
- Hospitalization decision -> Cost impact
- Follow-up intensity -> Cost correlation
- Recovery outcome -> Total cost

---

## Excel Interpretation Guide

### Sheet 1: Patient Data
Raw sample of 50 patient records showing all data fields

### Sheet 2: Summary
High-level KPIs:
- Total patients: 500
- Average age: ~52 years
- Average claim: $8,200
- Hospitalization rate: 24%

### Sheet 3: Condition Analysis
Breakdown by health condition:
- Condition names listed
- Average and total claims per condition
- Average recovery scores
- Patient counts per condition

### Sheet 4: Age Group Analysis
Performance by age ranges:
- 18-30, 31-50, 51-65, 65+
- Average claim amounts by age
- Average recovery scores
- Follow-up visit frequencies

### Sheet 5: Treatment Analysis
Effectiveness metrics per treatment type:
- Average recovery score
- Standard deviation (consistency)
- Average claim amount
- Average follow-up visits

### Sheet 6: Key Insights
Executive summary findings:
- Most expensive condition
- Most effective treatment
- High-need age group
- Cost multipliers (e.g., hospitalization impact)
- Most common diagnosis

---

## Creating Your Own Data Story

Use this template:
1. **Collect data** -> Create realistic dataset (like patient healthcare data)
2. **Analyze patterns** -> Find relationships and outliers
3. **Create Excel visualizations** -> Summary sheets, charts, analysis
4. **Design Graphviz diagrams** -> Show flows, relationships, categories
5. **Write narrative** -> Explain the story from insights
6. **Present conclusions** -> Actionable recommendations

This approach works for any domain:
- Sales pipelines and customer journeys
- Manufacturing production flows
- Software development lifecycles
- Financial transactions and fraud patterns
- Marketing campaign effectiveness
