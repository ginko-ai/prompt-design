graph TD
    A[Markdown Document] --> B[Section Headers]
    A --> C[YAML Content]

    B --> D[# Level 1]
    B --> E[## Level 2]
    B --> F[### Level 3]

    C --> G[PlantUML YAML Blocks]

    G --> H[@startyaml]
    G --> I[@endyaml]

    J[VSCode Features] --> K[Collapsible Headers]
    J --> L[PlantUML Preview]

    H --> M[Rendered YAML]
    I --> M

    style A fill:#f9f,stroke:#333
    style J fill:#bbf,stroke:#333
    style M fill:#bfb,stroke:#333


