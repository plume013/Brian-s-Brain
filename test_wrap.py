import numpy as np
from main import step

def test_wrap():
    # 3x3 grid
    # Place a firing cell at (1, 2) (right edge)
    # 0 0 0
    # 0 0 1
    # 0 0 0
    
    grid = np.zeros((3, 3), dtype=np.uint8)
    grid[1, 2] = 1
    
    # With wrap=True
    # The cell at (1, 0) (left edge) should have the cell at (1, 2) as a neighbor.
    # Let's check neighbor counts manually or just run step.
    # If we run step, (1, 0) has neighbors:
    # (0, -1)->(0,2)=0, (0, 0)->(0,0)=0, (0, 1)->(0,1)=0
    # (1, -1)->(1,2)=1,                  (1, 1)->(1,1)=0
    # (2, -1)->(2,2)=0, (2, 0)->(2,0)=0, (2, 1)->(2,1)=0
    # Total neighbors for (1, 0) = 1.
    
    # Wait, Brian's Brain birth rule is neighbor==2.
    # We need 2 neighbors to spawn.
    
    # Let's place two firing cells at the right edge to spawn something on the left edge.
    # 0 0 1
    # 0 0 1
    # 0 0 0
    grid = np.zeros((3, 3), dtype=np.uint8)
    grid[0, 2] = 1
    grid[1, 2] = 1
    
    # Target cell (0, 0) neighbors:
    # (-1,-1)->(2,2)=0, (-1,0)->(2,0)=0, (-1,1)->(2,1)=0
    # (0, -1)->(0,2)=1,                  (0, 1)->(0,1)=0
    # (1, -1)->(1,2)=1, (1, 0)->(1,0)=0, (1, 1)->(1,1)=0
    # Total = 2. So (0, 0) should become 1 (firing).
    
    print("Testing wrap=True...")
    next_grid = step(grid, wrap=True)
    
    if next_grid[0, 0] == 1:
        print("SUCCESS: Cell spawned at (0,0) due to wrapping neighbors at (0,2) and (1,2).")
    else:
        print("FAILURE: Cell did not spawn at (0,0). Wrap might be broken.")
        print("Grid state:\n", grid)
        print("Next grid:\n", next_grid)

    # Test wrap=False
    print("\nTesting wrap=False...")
    next_grid_no_wrap = step(grid, wrap=False)
    if next_grid_no_wrap[0, 0] == 0:
        print("SUCCESS: Cell did not spawn at (0,0) when wrap=False.")
    else:
        print("FAILURE: Cell spawned at (0,0) even when wrap=False.")

if __name__ == "__main__":
    test_wrap()
