class UIRegistry:

    def __init__(self):
        self._OBJECTS = {}

    def register(self, object_id, package, obj):
        self._OBJECTS[object_id] = [package, obj]

    def get(self, package, object_id):
        entry = self._OBJECTS.get(object_id)
        if entry is None:
            return None
        if entry[0] != package:
            return None
        return entry[1]

    def getPackage(self, object_id):
        entry = self._OBJECTS.get(object_id)
        return entry[0] if entry else None

    def unregister(self, object_id):
        return self._OBJECTS.pop(object_id, None)

    def exists(self, object_id):
        return object_id in self._OBJECTS