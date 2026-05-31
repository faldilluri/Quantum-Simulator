import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_bloch_vectors(vectors, labels, colors, title="Bloch Sphere"):
    """
    Vizualizon vektorë në sferën e Bloch duke përdorur matplotlib 3D.
    vectors: lista e [x, y, z] për secilin vektor
    labels: lista e etiketave
    colors: lista e ngjyrave
    """
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Vizato sferën
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.2, color='lightgray', edgecolor='none')
    
    # Vizato boshtet
    ax.quiver(0, 0, 0, 1.2, 0, 0, color='red', alpha=0.6, arrow_length_ratio=0.1, label='X')
    ax.quiver(0, 0, 0, 0, 1.2, 0, color='green', alpha=0.6, arrow_length_ratio=0.1, label='Y')
    ax.quiver(0, 0, 0, 0, 0, 1.2, color='blue', alpha=0.6, arrow_length_ratio=0.1, label='Z')
    
    # Vizato vektorët e dhënë
    for vec, label, color in zip(vectors, labels, colors):
        ax.quiver(0, 0, 0, vec[0], vec[1], vec[2], color=color, arrow_length_ratio=0.1, linewidth=2, label=label)
    
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig, ax

# ============================================================
# Për rastin konkret: |+⟩ dhe |-⟩
# |+⟩ = (1,0,0) në sferën Bloch
# |-⟩ = (-1,0,0)
# ============================================================
vectors = [[1, 0, 0], [-1, 0, 0]]
labels = ['|+⟩', '|-⟩']
colors = ['blue', 'orange']

fig, ax = plot_bloch_vectors(vectors, labels, colors, title="Z gate: |+⟩ → |-⟩")
plt.savefig('pauli_z_bloch_evolution.png', dpi=150)
plt.show()