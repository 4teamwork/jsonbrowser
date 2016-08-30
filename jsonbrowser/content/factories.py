from jsonbrowser.models.todo import Todo


class EntityFactory(object):

    model_class = None

    def __init__(self, data):
        self.data = data.copy()

    def resolve_relationships(self):
        pass

    def create(self):
        self.resolve_relationships()

        model_class = self.__class__.model_class
        if model_class is None:
            raise NotImplementedError

        entity = model_class(**self.data)
        return entity


class TodoFactory(EntityFactory):
    model_class = Todo
