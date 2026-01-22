# Text Summarization

## Description
Summarizes long text documents into concise summaries, extracting key points and main ideas.

## Category
Data Analysis

## Input Parameters
- `text`: The text content to summarize (string)
- `max_length`: Maximum length of the summary in words (optional, default: 100)
- `format`: Output format - "paragraph" or "bullet_points" (optional, default: "paragraph")

## Output
A concise summary of the input text in the specified format.

## Usage Example
```
Input:
  text: "A long article about climate change..."
  max_length: 50
  format: "bullet_points"

Output:
  • Climate change is accelerating globally
  • Major impacts include rising temperatures and sea levels
  • Immediate action required to mitigate effects
```

## Dependencies
- Natural language processing capability
- Text analysis tools

## Notes
- Works best with structured documents
- May require adjustment for technical or domain-specific content
- Supports multiple languages (quality may vary)
