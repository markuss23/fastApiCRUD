from pydantic import BaseModel

# co je potřeba zadat při vytvoření objektu.
class Student(BaseModel):
    """
    Schéma, které data jsou zapotřebí zadat při vytváření záznamu.
    Id chybí, protože je to primární klíč.
    """
    name: str
    email: str
    age: int
    country: str
