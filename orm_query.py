from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product, User, Cart, Banner
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

    products = result.scalars().all()
    for i in range(0, len(products)):
        products[i].page = i
    return products


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


async def orm_delete_product(session: AsyncSession, id_product: int):
    query = delete(Product).where(Product.id == id_product)
    await session.execute(query)
    await session.commit()


async def orm_add_user(session: AsyncSession, id_user: int):
    obj = User(
        id_user=id_user
    )
    session.add(instance=obj)
    await session.commit()


####################### Корзина ########################################################################


async def orm_add_product_in_cart(session: AsyncSession, id_user: int, id_product: int):
    obj = Cart(
        id_user=id_user,
        id_product=id_product
    )
    session.add(instance=obj)
    await session.commit()


async def orm_get_all_products_in_cart(session: AsyncSession, id_user):
    query = select(Cart).where(Cart.id_user == id_user)
    result = await session.execute(query)
    products = result.scalars().all()
    for i in range(0, len(products)):
        products[i].page = i
    return products


async def orm_get_one_in_cart(session: AsyncSession, id_user: int, id_product: int):
    query = select(Cart).where(Cart.id_user == id_user and Cart.id_product == id_product)
    result = await session.execute(query)
    return result.scalar()


async def orm_del_product_in_cart(session: AsyncSession, id_product: int):
    query = delete(Cart).where(Cart.id == id_product)
    await session.execute(query)
    await session.commit()


async def orm_del_all_products_in_cart(session: AsyncSession, id_users):
    query = delete(Cart).where(Cart.id_user == id_users)
    await session.execute(query)
    await session.commit()


################################### banner ###################################################


async def orm_add_banner(session: AsyncSession, photo: str):
    query = select(Banner).where(Banner.id == 1)
    result = await session.execute(query)

    if result.first() is None:
        session.add(
            Banner(photo=photo)
        )
        await session.commit()
    else:
        query = update(Banner).where(Banner.id == 1).values(
            photo=photo
        )
        await session.execute(query)
        await session.commit()



async def orm_get_banner(session: AsyncSession):
    query = select(Banner).where(Banner.id == 1)
    result = await session.execute(query)
    return result.scalar()