# Just Fun, a creative script to draw a dream catcher with user-input dreams displayed within it.
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

def draw_dream_catcher_with_text(dreams_list):
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Set background color
    fig.patch.set_facecolor('#1a0b2e')
    ax.set_facecolor('#1a0b2e')

    # Draw the outer circle with gradient effect using multiple circles
    colors_gradient = ['#8B4513', '#A0522D', '#CD853F', '#DEB887']
    for i, color in enumerate(colors_gradient):
        radius = 4 - (i * 0.05)
        outer_circle = patches.Circle((5, 6), radius, edgecolor=color, 
                                     facecolor='none', lw=4-i, alpha=0.8)
        ax.add_patch(outer_circle)
    
    # Fill the circle with a nice color
    inner_fill = patches.Circle((5, 6), 3.8, facecolor='#F4A460', alpha=0.6)
    ax.add_patch(inner_fill)

    # Draw the inner web with more lines
    num_lines = 16
    for i in range(num_lines):
        angle = 2 * np.pi / num_lines * i
        x_end = 5 + 3.8 * np.cos(angle)
        y_end = 6 + 3.8 * np.sin(angle)
        ax.plot([5, x_end], [6, y_end], color='#8B4513', lw=1.5, alpha=0.7)

    # Draw concentric circles for the web
    for r in np.linspace(0.5, 3.5, 8):
        web_circle = patches.Circle((5, 6), r, edgecolor='#A0522D', 
                                   facecolor='none', lw=1.5, alpha=0.6)
        ax.add_patch(web_circle)
    
    # Add decorative beads on the circle
    bead_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFD93D']
    bead_angles = [0, np.pi/2, np.pi, 3*np.pi/2]
    for angle, color in zip(bead_angles, bead_colors):
        bead_x = 5 + 3.8 * np.cos(angle)
        bead_y = 6 + 3.8 * np.sin(angle)
        bead = patches.Circle((bead_x, bead_y), 0.15, facecolor=color, 
                             edgecolor='white', lw=1)
        ax.add_patch(bead)
    
    # Center hole
    center_hole = patches.Circle((5, 6), 0.3, facecolor='#2d1b4e', 
                                edgecolor='#8B4513', lw=2)
    ax.add_patch(center_hole)

    # Add user dreams randomly within the circle
    colors_text = ['#FF1493', '#00CED1', '#FFD700', '#FF6347', 
                   '#9370DB', '#32CD32', '#FF69B4', '#4169E1']
    
    # Track occupied positions to avoid overlap
    occupied_positions = []
    
    def is_position_available(x, y, occupied, min_distance=0.8):
        """Check if position is far enough from other texts"""
        for (ox, oy) in occupied:
            distance = np.sqrt((x - ox)**2 + (y - oy)**2)
            if distance < min_distance:
                return False
        return True
    
    for i, dream_text in enumerate(dreams_list):
        # Try to find a non-overlapping position
        max_attempts = 50
        position_found = False
        
        for attempt in range(max_attempts):
            # Generate random position within the circle
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(0.8, 3.0)
            text_x = 5 + radius * np.cos(angle)
            text_y = 6 + radius * np.sin(angle)
            
            # Check if position is available
            if is_position_available(text_x, text_y, occupied_positions):
                position_found = True
                occupied_positions.append((text_x, text_y))
                break
        
        # If no position found after attempts, use spiral placement
        if not position_found:
            spiral_angle = i * 2.4  # Golden angle approximation
            spiral_radius = 0.8 + (i * 0.3)
            text_x = 5 + spiral_radius * np.cos(spiral_angle)
            text_y = 6 + spiral_radius * np.sin(spiral_angle)
            occupied_positions.append((text_x, text_y))
        
        # Random rotation for text
        rotation = np.random.uniform(-15, 15)
        
        # Color selection
        text_color = colors_text[i % len(colors_text)]
        
        # Adjust font size based on text length
        font_size = max(8, min(11, 100 // len(dream_text)))
        
        ax.text(text_x, text_y, dream_text, 
               fontsize=font_size, color=text_color, 
               ha='center', va='center', 
               rotation=rotation,
               weight='bold',
               style='italic',
               bbox=dict(boxstyle='round,pad=0.3', 
                        facecolor='white', 
                        alpha=0.7,
                        edgecolor=text_color,
                        linewidth=1.5))

    # Add title
    ax.text(5, 11.2, '✨ My Dream Catcher ✨', 
           fontsize=20, color='#FFD700', 
           ha='center', va='center', weight='bold',
           style='italic')
    
    plt.tight_layout()
    plt.show()

# Main program
print("=" * 50)
print("🌙 ✨ DREAM CATCHER CREATOR ✨ 🌙")
print("=" * 50)
print("\nAdd your dreams, wishes, and aspirations!")
print("Type 'done' when you're finished adding dreams.\n")

dreams = []

while True:
    user_input = input(f"Enter dream #{len(dreams) + 1} (or 'done' to finish): ").strip()
    
    if user_input.lower() == 'done':
        if dreams:
            print(f"\n✨ Creating your dream catcher with {len(dreams)} dream(s)...")
            draw_dream_catcher_with_text(dreams)
            
            # Ask if they want to create another
            again = input("\nWould you like to create another dream catcher? (yes/no): ").strip().lower()
            if again == 'yes' or again == 'y':
                dreams = []
                print("\n" + "=" * 50)
                print("Starting new dream catcher...")
                print("=" * 50 + "\n")
            else:
                print("\n✨ Thank you for using Dream Catcher Creator! ✨")
                break
        else:
            print("Please add at least one dream before finishing!")
    elif user_input:
        dreams.append(user_input)
        print(f"✓ Dream added! ({len(dreams)} total)")
    else:
        print("Please enter some text or type 'done' to finish.")
