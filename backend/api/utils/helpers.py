from fastapi import HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query


def get_object_by_id(model: declarative_base, path_variable: int, db: sessionmaker):
    """Get a single object from a model by its ID

    Args:
        model (declarative_base): The model to fetch the object
        path_variable (int): The path_variable with the id
        db (sessionmaker): The database session

    Raises:
        HTTPException: If an object with the provided ID is not found

    Returns:
        _type_: The object instance
    """
    instance = db.query(model).filter(model.id == path_variable).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="Object not found")
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
