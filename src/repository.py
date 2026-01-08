"""Repository management."""
import os

class Repository:
    def __init__(self, path):
        self.path = path
        self.git_dir = os.path.join(path, '.git')

    def init(self):
        """Initialize new repository."""
        os.makedirs(os.path.join(self.git_dir, 'objects'), exist_ok=True)
        os.makedirs(os.path.join(self.git_dir, 'refs', 'heads'), exist_ok=True)

        # Create HEAD
        with open(os.path.join(self.git_dir, 'HEAD'), 'w') as f:
            f.write('ref: refs/heads/main\n')
