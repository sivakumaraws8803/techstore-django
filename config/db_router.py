class SharedProductRouter:
    """
    Route SharedProduct queries to the existing PostgreSQL database.
    Keep all other Django models on SQLite.
    """

    route_app_labels = {"products"}

    def db_for_read(self, model, **hints):
        if model.__name__ == "SharedProduct":
            return "shared_products"
        return None

    def db_for_write(self, model, **hints):
        if model.__name__ == "SharedProduct":
            return "shared_products"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1.__class__.__name__ == "SharedProduct"
            or obj2.__class__.__name__ == "SharedProduct"
        ):
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "products" and model_name == "sharedproduct":
            return False
        return None
