# Helicon Geometry Project Context Document

## Current Project State
The project has evolved from 2D geometric construction to 3D spatial analysis, with the following major components implemented:

### 1. Base 2D Construction (Completed)
- Standard Cartesian coordinate system (-10 to 10)
- Base circle centered at origin
- Square with diagonals
- Four semicircles at cardinal points
- Triangle lines forming intersection patterns
- Harmonic ratio lines
- Intersection points (color-coded)

### 2. 3D Implementation (Current)
- Three perpendicular faces of a cube containing the 2D pattern
- Projection lines extending inward from intersection points
- Triple intersection detection system
- Color coding scheme:
  - Light green: Standard intersection points
  - Purple: Triple intersection points
  - Gray: Projection lines
  - Standard colors for geometric elements

### 3. Core Components

#### File Structure
- helicon_geometry-v9.4.py: Original 2D implementation
- helicon-svgConstruction.svg: 2D visualization
- Updated 3D implementation with intersection detection

#### Key Classes and Functions
```python
def find_triple_intersections(points_xy, points_yz, points_xz)
def create_cube_faces()
def transform_intersection_points(points, plane='xy')
def create_helicon_pattern(plane='xy', triple_intersections=None)
def visualize_3d_helicon()
```

#### Intersection Point Sets
Normalized coordinates for unit cube:
- Central axis points: [0, ±0.5, 0], [±0.5, 0, 0]
- Left/Right clusters: [±0.6, ±0.2, 0], [±0.333, ±0.333, 0], [±0.2, ±0.6, 0]

## Current Focus
- Detection and visualization of points where projection lines from all three faces intersect
- Color-coding system for distinguishing different types of intersections
- Geometric analysis of spatial relationships

## Next Steps
Potential areas for expansion:
1. Automated analysis of triple intersection patterns
2. Mathematical relationship documentation between 2D and 3D intersections
3. Integration with geometric theorem proving
4. Development of interactive visualization tools

## Technical Requirements
- Python 3.x
- Open3D library
- NumPy for calculations
- SVG capability for 2D visualizations

## Reference Documents
1. helicon_geometry-v2-context.md: Base construction rules
2. helicon_geometry-v9.4.md: Class diagram
3. helicon-svgConstruction.svg: 2D reference visualization

## Notes on Intersection Detection
- Tolerance value: 0.01 for intersection detection
- Validation of points within unit cube bounds
- Triple intersections require convergence from all three perpendicular faces
- Projection lines extend inward from surface points

## Visualization Guidelines
1. Main geometric elements:
   - Cube edges: Gray
   - Base patterns: Original colors from 2D
   - Intersection points: Light green/Purple
   - Projection lines: Gray
2. Camera positioning:
   - Default view: [-0.5, -0.5, -0.5]
   - Up vector: [0, 0, 1]
   - Zoom level: 0.8

## Known Constraints
1. Intersection detection limited by numerical precision
2. Visual clarity depends on viewing angle
3. Performance considerations with large numbers of projection lines

## Future Considerations
1. Implementation of additional geometric relationships
2. Enhanced intersection analysis tools
3. Documentation of mathematical proofs
4. Integration with larger geometric systems