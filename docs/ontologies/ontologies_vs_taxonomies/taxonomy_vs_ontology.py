from typing import Dict, List, Optional, Set
from dataclasses import dataclass

# Taxonomy Implementation
class TaxonomyNode:
    def __init__(self, name: str):
        self.name = name
        self.children: List[TaxonomyNode] = []
        self.parent: Optional[TaxonomyNode] = None

    def add_child(self, child: 'TaxonomyNode') -> None:
        self.children.append(child)
        child.parent = self

    def get_ancestors(self) -> List[str]:
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current.name)
            current = current.parent
        return ancestors

# Ontology Implementation
@dataclass
class Relationship:
    relation_type: str
    target_entity: str
    properties: Dict[str, str] = None

class OntologyEntity:
    def __init__(self, name: str):
        self.name = name
        self.relationships: List[Relationship] = []
        self.properties: Dict[str, str] = {}

    def add_relationship(self, relation_type: str, target: str,
                        properties: Dict[str, str] = None) -> None:
        self.relationships.append(
            Relationship(relation_type, target, properties)
        )

    def add_property(self, key: str, value: str) -> None:
        self.properties[key] = value

    def get_related_entities(self, relation_type: Optional[str] = None) -> Set[str]:
        if relation_type:
            return {rel.target_entity for rel in self.relationships
                    if rel.relation_type == relation_type}
        return {rel.target_entity for rel in self.relationships}

# Example Usage
def create_animal_taxonomy() -> TaxonomyNode:
    root = TaxonomyNode("Animal")
    mammal = TaxonomyNode("Mammal")
    bird = TaxonomyNode("Bird")

    root.add_child(mammal)
    root.add_child(bird)

    mammal.add_child(TaxonomyNode("Cat"))
    mammal.add_child(TaxonomyNode("Dog"))

    return root

def create_cat_ontology() -> OntologyEntity:
    cat = OntologyEntity("Cat")

    # Add properties
    cat.add_property("average_lifespan", "12-18 years")
    cat.add_property("domestication_period", "~9,000 years ago")

    # Add relationships
    cat.add_relationship("is-a", "Mammal")
    cat.add_relationship("has", "Fur", {"type": "physical_characteristic"})
    cat.add_relationship("lives-in", "Home", {"typical": "yes"})
    cat.add_relationship("eats", "Fish", {"preference": "high"})

    return cat
    