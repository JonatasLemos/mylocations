import math

from fastapi import HTTPException
from sqlalchemy import literal_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query


def get_object_by_id(
    model: declarative_base,
    path_variable: int,
    db: sessionmaker,
    status_code: int = 404,
    msg: str = "Object not found",
):
    """Get a single object from a model by its ID

    Args:
        model (declarative_base): The model to fetch the object
        path_variable (int): The path_variable with the id
        db (sessionmaker): The database session
        status_code (int, optional): The status code to return if
        the object is not found. Defaults to 404.
        msg: The message to return if the object is not found.
        Defaults to "Object not found".

    Raises:
        HTTPException: If an object with the provided ID is not found

    Returns:
        _type_: The object instance
    """
    instance = db.query(model).filter(model.id == path_variable).first()
    if instance is None:
        raise HTTPException(status_code=status_code, detail=msg)
    return instance


def order_objects(
    model: declarative_base,
    order_by_param: str,
    order_param: str,
    query: Query,
) -> Query:
    """Order objects in a model, given the order_by column and order direction

    Args:
        model (declarative_base): The model to order
        order_by_param (str): The column to order by
        order_param (str): The order direction
        query (Query): The model query

    Raises:
        HTTPException: If the order_by column does not exist

    Returns:
        Query: The ordered query
    """
    column = getattr(model, order_by_param, None)
    if column is None:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid order_by column: {order_by_param}",
        )
    if order_param.lower() == "desc":
        return query.order_by(column.desc())
    return query.order_by(column)


def order_objects_with_literals(
    order_by_column: str, order_param: str, query: Query
) -> Query:
    """Order objects when literal_column is needed

    Args:
        order_by_column (str): The column to order by
        order_param (str): The order direction
        query (Query): The model query

    Returns:
        Query: The ordered query
    """
    if order_param.lower() == "desc":
        return query.order_by(literal_column(order_by_column).desc())
    return query.order_by(literal_column(order_by_column))


class CustomPaginator:
    """Paginate query using size and page from query parameters."""

    def __init__(self, query: Query, page: int, size: int):
        """Initializer method

        Args:
            query (Query): The query to paginate
            page (int): The pages to use in offset
            size (int): The page size
        """
        self.query = query
        self.page = page
        self.size = size
        self.pages: int = None
        self.total: int = None

    def paginate_query(self) -> list:
        """Paginate query and return the final paginated items.

        Returns:
            list: The final paginated items
        """
        self.total = self.query.count()
        self.pages = math.ceil(self.total / self.size)
        offset = (self.page - 1) * self.size
        return self.query.offset(offset).limit(self.size).all()
