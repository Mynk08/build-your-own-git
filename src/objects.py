"""Git object database implementation."""
import hashlib
import zlib
import os

class GitObject:
    def __init__(self, data=None, obj_type='blob'):
        self.data = data
        self.obj_type = obj_type

    def serialize(self):
        """Serialize object for storage."""
        header = f'{self.obj_type} {len(self.data)}\0'
        return header.encode() + self.data

    def hash(self):
        """Calculate SHA-1 hash of object."""
        content = self.serialize()
        return hashlib.sha1(content).hexdigest()

    def write(self, repo_path):
        """Write object to repository."""
        sha = self.hash()
        obj_dir = os.path.join(repo_path, '.git', 'objects', sha[:2])
        os.makedirs(obj_dir, exist_ok=True)

        obj_path = os.path.join(obj_dir, sha[2:])
        with open(obj_path, 'wb') as f:
            f.write(zlib.compress(self.serialize()))
        return sha

class Blob(GitObject):
    def __init__(self, data):
        super().__init__(data, 'blob')

class Tree(GitObject):
    def __init__(self, entries):
        self.entries = entries
        super().__init__(self._serialize_entries(), 'tree')

    def _serialize_entries(self):
        result = b''
        for mode, name, sha in sorted(self.entries):
            result += f'{mode} {name}\0'.encode()
            result += bytes.fromhex(sha)
        return result
