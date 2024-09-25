from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product
from sqlalchemy import select, update, delete


async def orm_add_product(session: AsyncSession, data: dict):
    obj = Product(
        title=data['title'],
        description=data['description'],
        price=float(data['price']),
        photo=data['photo']
    )
    session.add(instance=obj)
    await session.commit()


async def orm_get_products(session: AsyncSession):
    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_one(session: AsyncSession, id_product: int):
    query = select(Product).where(Product.id == id_product)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_product(session: AsyncSession, id_product: int, data):
    query = update(Product).where(Product.id == id_product).values(
        title=data['title'],
        description=data['description'],
        price=float(data['price']),
        photo=data['photo']
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_product(sesion: AsyncSession, id_product: int):
    query = delete(Product).where(Product.id == id_product)
    await sesion.execute(query)
    await sesion.commit()