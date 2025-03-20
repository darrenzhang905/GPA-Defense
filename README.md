# GPA-Defense

This is a simple tower defense game that me and my friends programmed during a 24 hour hackathon.

## Description

GPA Defense is a tower defense style game where you protect your GPA from incoming enemies. As enemies reach the end of the path, they decrease your GPA. Your goal is to strategically place towers to defend your academic standing while managing your DineX (in-game currency).

## Setup Instructions

### Setting up a Python Environment

1. Create a new virtual environment:

   ```
   python -m venv gpadefense_env
   ```

2. Activate virtual environment:

   ```
   source gpadefense_env/bin/activate
   ```

### Installing Dependencies

Once your Python environment is set up and activated, install the required packages:

```
pip install -r requirements.txt
```

## How to run

After setting up your environment and installing dependencies:

1. Run the game file:
   ```
   python dino_run.py
   ```

## Key Features

- **Multiple Tower Types**: Different towers with unique abilities, attack speeds, and damage values
- **Resource Management**: Balance your DineX spending to build an effective defense strategy
- **GPA Tracking**: Watch your GPA and protect it from dropping due to enemies
- **CMU Theme**: Features familiar CMU locations as tower types (Wean, Gates, CFA, Tent)

## Game Mechanics

### Resources

- **GPA**: Starts at 4.0 and decreases as enemies reach the end of the path
- **DineX**: In-game currency used to purchase and place towers
  - Earn 100 DineX for each enemy destroyed
  - Starting value: 20,000

### Tower Types

1. **Wean Tower**

   - Cost: 500 DineX
   - Damage: 5
   - Fire Rate: 1
   - Range: 2 cell radius

2. **Tent Tower**

   - Cost: 250 DineX
   - Damage: 2
   - Fire Rate: 1
   - Range: 2 cell radius

3. **CFA Tower**

   - Cost: 1000 DineX
   - Damage: 1
   - Fire Rate: 1
   - Range: 2 cell radius
   - Special: Can damage multiple enemies in range

4. **Gates Tower**
   - Cost: 1500 DineX
   - Damage: 20
   - Fire Rate: 5
   - Range: 2 cell radius
   - Special: High damage but slower fire rate

### Enemies

- Each enemy follows a set path through the game board
- Enemies have health proportional to their grade value
- When destroyed, enemies give you 100 DineX
- When reaching the end, enemies decrease your GPA by 0.01

## Controls

- **W Key**: Select Wean Tower for placement
- **T Key**: Select Tent Tower for placement
- **C Key**: Select CFA Tower for placement
- **G Key**: Select Gates Tower for placement
- **Spacebar**: Spawn a new enemy (for testing)
- **Mouse Click**: Place selected tower on valid terrain
- **ESC Key**: Cancel tower placement / Deselect tower

## Game Interface

- The main game board is displayed on the left side (750x750 pixels)
- Tower information and controls are shown in the right sidebar
- Blue outlines indicate valid placement locations
- Red outlines indicate invalid placement locations
