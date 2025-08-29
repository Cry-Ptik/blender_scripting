"""
Comprehensive mock Blender API for CLI usage.
Provides all necessary bpy attributes and methods to avoid import errors.
"""

class MockMaterial:
    def __init__(self, name="Material"):
        self.name = name
        self.use_nodes = True
        self.node_tree = MockNodeTree()

class MockMesh:
    def __init__(self, name="Mesh"):
        self.name = name
        self.vertices = []
        self.faces = []
    
    def from_pydata(self, vertices, edges, faces):
        """Mock method for creating mesh from Python data."""
        self.vertices = vertices
        self.faces = faces
    
    def update(self):
        """Mock method for updating mesh."""
        pass

class MockObject:
    def __init__(self, name="Object"):
        self.name = name
        self.data = None
        self.location = [0, 0, 0]
        self.rotation_euler = [0, 0, 0]
        self.scale = [1, 1, 1]

class MockNode:
    def __init__(self):
        self.inputs = {}
        self.outputs = {}

class MockNodeTree:
    def __init__(self):
        self.nodes = MockNodes()
        self.links = MockLinks()

class MockNodes:
    def new(self, node_type):
        return MockNode()
    
    def remove(self, node):
        pass

class MockLinks:
    def new(self, output, input):
        pass

class MockScene:
    def __init__(self):
        self.name = "Scene"
        self.collection = MockSceneCollection()

class MockViewLayer:
    def __init__(self):
        self.name = "ViewLayer"

class MockSceneCollection:
    def __init__(self):
        self.name = "Collection"
        self.objects = MockObjectLinker()
        self.children = MockCollectionLinker()

class MockObjectLinker:
    def __init__(self):
        self.items = []
    
    def link(self, obj):
        """Mock method for linking objects to collection."""
        self.items.append(obj)

class MockCollectionLinker:
    def __init__(self):
        self.items = []
    
    def link(self, collection):
        """Mock method for linking collections."""
        self.items.append(collection)

class MockContext:
    def __init__(self):
        self.scene = MockScene()
        self.view_layer = MockViewLayer()
        self.collection = MockSceneCollection()

class MockCollection:
    def __init__(self):
        self.items = []
    
    def new(self, name, *args):
        if hasattr(self, '_item_class'):
            item = self._item_class(name)
        else:
            item = MockObject(name)
        self.items.append(item)
        return item
    
    def __iter__(self):
        return iter(self.items)
    
    def __len__(self):
        return len(self.items)

class MockMeshCollection(MockCollection):
    def __init__(self):
        super().__init__()
        self._item_class = MockMesh

class MockObjectCollection(MockCollection):
    def __init__(self):
        super().__init__()
        self._item_class = MockObject

class MockMaterialCollection(MockCollection):
    def __init__(self):
        super().__init__()
        self._item_class = MockMaterial

class MockImageCollection(MockCollection):
    def __init__(self):
        super().__init__()
        self._item_class = MockImage

class MockDataSceneCollection(MockCollection):
    def __init__(self):
        super().__init__()
        self._item_class = MockSceneCollection

class MockData:
    def __init__(self):
        self.materials = MockMaterialCollection()
        self.meshes = MockMeshCollection()
        self.objects = MockObjectCollection()
        self.images = MockImageCollection()
        self.collections = MockDataSceneCollection()

class MockImage:
    def __init__(self, name="Image"):
        self.name = name
        self.size = [1024, 1024]
        self.pixels = []

class MockTexture:
    def __init__(self, name="Texture"):
        self.name = name
        self.image = None

class MockTypes:
    Material = MockMaterial
    Mesh = MockMesh
    Object = MockObject
    Scene = MockScene
    ViewLayer = MockViewLayer
    ShaderNodeTree = MockNodeTree
    Node = MockNode
    Image = MockImage
    Texture = MockTexture
    
    # Add any missing types as needed
    def __getattr__(self, name):
        # Return a generic mock class for any missing type
        return type(name, (), {})

class MockMaterialOps:
    @staticmethod
    def new():
        return MockMaterial()

class MockMeshOps:
    @staticmethod
    def primitive_plane_add(**kwargs):
        pass

class MockObjectOps:
    @staticmethod
    def select_all(**kwargs):
        pass
    
    @staticmethod
    def delete(**kwargs):
        pass

class MockView3DOps:
    @staticmethod
    def view_all(**kwargs):
        pass

class MockOps:
    def __init__(self):
        self.material = MockMaterialOps()
        self.mesh = MockMeshOps()
        self.object = MockObjectOps()
        self.view3d = MockView3DOps()

class MockPath:
    @staticmethod
    def abspath(path):
        import os
        # Convert Blender-style relative paths to absolute paths
        if path.startswith("//"):
            # Remove the // prefix and make it relative to current directory
            path = path[2:]
        return os.path.abspath(path)
    
    @staticmethod
    def dirname(path):
        import os
        return os.path.dirname(path)
    
    @staticmethod
    def basename(path):
        import os
        return os.path.basename(path)
    
    @staticmethod
    def join(*args):
        import os
        return os.path.join(*args)

class MockBpy:
    def __init__(self):
        self.data = MockData()
        self.context = MockContext()
        self.types = MockTypes()
        self.ops = MockOps()
        self.path = MockPath()

# Create the mock bpy instance
mock_bpy = MockBpy()
