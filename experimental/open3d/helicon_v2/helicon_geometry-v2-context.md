# Helicon Geometry Construction Rules

## Coordinate System
- Standard Cartesian coordinate system with (x,y) format
- Origin at center (0,0)
- Point (10,10) positioned at upper right
- Positive x points right
- Positive y points up
- Grid spans from -10 to 10 in both x and y directions

## Base Layer: Circle
- Circle centered at origin (0,0)
- Radius = 10 units
- Color: Blue

## Layer 1: Square and Diagonals
- Square with corners at:
  - Upper right: (10,10)
  - Upper left: (-10,10)
  - Lower right: (10,-10)
  - Lower left: (-10,-10)
- Diagonals connecting opposite corners
- Color: Green
- Red dots mark:
  - Square corners
  - Circle-square intersections at (±10,0) and (0,±10)

## Layer 2: Semi-circles
- Four semi-circles, each with radius 10 units
- Centers at circle-square intersections:
  - Right: (10,0)
  - Left: (-10,0)
  - Top: (0,10)
  - Bottom: (0,-10)
- All semi-circles contained within the square
- All semi-circles intersect at origin (0,0)
- Color: Light blue

## Layer 3: Triangle Lines
Eight orange lines forming four triangular patterns (T1-T4):

T1:
- Line1: (-10,10) to (0,-10)
- Line2: (10,10) to (0,-10)

T2:
- Line4: (-10,-10) to (10,0)
- Line5: (-10,10) to (10,0)

T3:
- Line7: (10,-10) to (0,10)
- Line8: (-10,-10) to (0,10)

T4:
- Line10: (10,-10) to (-10,0)
- Line11: (10,10) to (-10,0)
Color: Orange

## Layer 4: Intersection Points
Purple dots at intersections of orange lines:
- Horizontal row: (-5,0), (0,0), (5,0)
- Vertical column: (0,5), (0,-5)

Note: Corner intersection points at (±5,±5) are explicitly excluded

## Visual Properties
- Grid lines: Light gray
- Coordinate axes: Black with arrows
- Circle: Blue
- Square and diagonals: Green
- Semi-circles: Light blue
- Triangle lines: Orange
- Major intersection points: Red
- Line intersection points: Purple

## Key Intersection Types
1. Square corners (red)
2. Circle-square intersections (red)
3. Line intersections (purple)
4. Origin point (purple)