"""
@startuml
title MarkdownYAMLConverter Class Diagram

class MarkdownYAMLConverter {
    - yaml_block_pattern: Pattern
    + __init__()
    + extract_yaml_blocks(content: str): List[Tuple]
    + convert_yaml_to_plantuml(yaml_content: str): str
    + convert_document(filepath: str): str
    + save_converted_document(input_path: str, output_path: str): void
}

class "YAML Block" as YB {
    + pre_content: str
    + yaml_content: str
    + post_content: str
}

class "PlantUML Block" as PB {
    + start_tag: String
    + content: String
    + end_tag: String
}

note right of PB
  In actual implementation:
  start_tag = (at)startyaml
  end_tag = (at)endyaml
  where (at) represents @
end note

MarkdownYAMLConverter ..> YB: extracts
MarkdownYAMLConverter ..> PB: creates
YB ..> PB: converts to

@enduml
"""


import re
from typing import List, Tuple
import yaml

class MarkdownYAMLConverter:
    """Converts markdown documents with YAML blocks to PlantUML-compatible format."""

    def __init__(self):
        self.yaml_block_pattern = re.compile(r'```yaml\n(.*?)\n```', re.DOTALL)

    def extract_yaml_blocks(self, content: str) -> List[Tuple[str, str, str]]:
        """
        Extracts YAML blocks and their surrounding context.

        Args:
            content: The markdown document content

        Returns:
            List of tuples containing (pre_content, yaml_block, post_content)
        """
        positions = []
        for match in self.yaml_block_pattern.finditer(content):
            start, end = match.span()
            yaml_content = match.group(1)
            positions.append((
                content[:start],
                yaml_content,
                content[end:]
            ))
        return positions

    def convert_yaml_to_plantuml(self, yaml_content: str) -> str:
        """
        Converts YAML content to PlantUML format.

        Args:
            yaml_content: The YAML block content

        Returns:
            PlantUML-formatted YAML content
        """
        # Validate YAML first
        try:
            yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML content: {e}")

        # Format for PlantUML
        return f"@startyaml\n{yaml_content}\n@endyaml"

    def convert_document(self, filepath: str) -> str:
        """
        Converts entire document to PlantUML-compatible format.

        Args:
            filepath: Path to the markdown document

        Returns:
            Converted document content
        """
        with open(filepath, 'r') as f:
            content = f.read()

        # Process each YAML block
        blocks = self.extract_yaml_blocks(content)
        converted_content = content

        for pre, yaml_block, post in blocks:
            plantuml_block = self.convert_yaml_to_plantuml(yaml_block)
            converted_content = converted_content.replace(
                f"```yaml\n{yaml_block}\n```",
                plantuml_block
            )

        return converted_content

    def save_converted_document(self, input_path: str, output_path: str):
        """
        Converts and saves document with preserved formatting.

        Args:
            input_path: Source markdown file path
            output_path: Destination file path
        """
        converted = self.convert_document(input_path)
        with open(output_path, 'w') as f:
            f.write(converted)


if __name__ == "__main__":
    converter = MarkdownYAMLConverter()
    converter.save_converted_document(
        "logseq-yaml-documentation.md",
        "logseq-yaml-documentation-plantuml.md"
    )
