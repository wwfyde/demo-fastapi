import asyncio
import time
from datetime import datetime
from logging import getLogger
from typing import Type, TypeVar

from sqlalchemy import bindparam, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Session


from demo_fastapi.core.db import async_engine, engine
from demo_fastapi.models.product import Product, ProductDetail, ProductReview, ProductSKU

logger = getLogger(__name__)

T = TypeVar("T", bound=DeclarativeBase)


def field_filter(model: Type[T], data: dict | list[dict]) -> list[dict]:
    """
    过滤字段, 仅当字段存在于表中才会保存
    """
    if isinstance(data, dict):
        data = [data]
    new_data = []
    for item in data:
        new_data.append({key: value for key, value in item.items() if key in model.__table__.columns})
    return new_data

    # return {key: value for key, value in data.items() if key in model.__table__.columns}


def save_review_data(data: dict | list[dict]):
    """
    保存数据为json 和数据库
    主语
    """
    start_time = time.time()  # 开始计时

    if isinstance(data, dict):
        data = [data]

    data: list = field_filter(ProductReview, data)

    with Session(engine) as session:
        inserted_ids = []
        for item in data:
            review_id = item.get("review_id")
            source = item.get("source")
            ...
            if review_id is None:
                logger.error("review_id is None")
                continue

            review = (
                session.execute(
                    select(ProductReview).filter(ProductReview.review_id == review_id, ProductReview.source == source)
                )
                .scalars()
                .one_or_none()
            )
            if review:
                for key, value in item.items():
                    setattr(review, key, value)
                session.add(review)
                session.commit()
                session.refresh(review)
                logger.debug(
                    f"更新评论[review]数据成功, id={review.id},review_id={review.review_id} , product_id={review.product_id}, source={review.source}"
                )
                if review.product_id != item.get("product_id"):
                    logger.error(f"product_id 不一致, {review.product_id} != {item.get('product_id')}")
                inserted_ids.append(review.id)
            else:
                stmt = insert(ProductReview).values(item)
                review = session.execute(stmt)
                # log.warning(review)
                insert_id = review.inserted_primary_key[0] if review.inserted_primary_key else None
                # log.warning(insert_id)
                session.commit()
                if insert_id:
                    inserted_ids.append(insert_id)
                    review = (
                        session.execute(select(ProductReview).filter(ProductReview.id == insert_id))
                        .scalars()
                        .one_or_none()
                    )

                    logger.debug(
                        f"插入评论[review]数据成功, id={review.id}, product_id={review.product_id}, source={review.source}"
                    )
        end_time = time.time()  # 结束计时
        logger.debug(f"保存评论[review]数据完成，耗时 {end_time - start_time:.2f} 秒")
        return inserted_ids if inserted_ids else None


def save_sku_data(data: dict | list[dict]) -> list | None:
    """
    保存数据为json 和数据库
    """
    start_time = time.time()
    if isinstance(data, dict):
        data = [data]
    data: list = field_filter(ProductSKU, data)
    inserted_ids = []
    with Session(engine) as session:
        for item in data:
            sku_id = item.get("sku_id")
            source = item.get("source")
            product_id = item.get("product_id")

            sku = (
                session.execute(
                    select(ProductSKU).filter(
                        ProductSKU.sku_id == sku_id, ProductSKU.source == source, ProductSKU.product_id == product_id
                    )
                )
                .scalars()
                .one_or_none()
            )
            if sku:
                for key, value in item.items():
                    setattr(sku, key, value)
                session.add(sku)
                session.commit()
                session.refresh(sku)
                logger.debug(
                    f"更新子款[SKU] 数据成功, id={sku.id}, sku_id={sku.sku_id}, product_id={sku.product_id}, source={sku.source}"
                )
                inserted_ids.append(sku.id)
            else:
                stmt = insert(ProductSKU).values(item)
                result = session.execute(stmt)
                session.commit()
                insert_id = result.inserted_primary_key[0] if result.inserted_primary_key else None
                if insert_id:
                    inserted_ids.append(insert_id)
                    sku = session.execute(select(ProductSKU).filter(ProductSKU.id == insert_id)).scalars().one_or_none()
                    logger.debug(
                        f"插入子款[SKU] 数据成功, id={sku.id}, sku_id={sku.sku_id}, product_id={sku.product_id}, source={sku.source}"
                    )
        end_time = time.time()  # 结束计时
        logger.debug(f"保存子款[sku]数据完成，耗时 {end_time - start_time:.2f} 秒")
        return inserted_ids if inserted_ids else None


def save_product_data(data: dict | list[dict]):
    """
    保存数据为json 和数据库
    """
    start_time = time.time()
    if isinstance(data, dict):
        data = [data]
    data: list = field_filter(Product, data)
    inserted_ids = []
    with Session(engine) as session:
        for item in data:
            product_id = item.get("product_id")
            source = item.get("source")
            product = (
                session.execute(
                    select(Product).filter(
                        Product.product_id == product_id,
                        Product.source == source,
                    )
                )
                .scalars()
                .one_or_none()
            )
            if product:
                for key, value in item.items():
                    setattr(product, key, value)
                session.add(product)
                session.commit()
                session.refresh(product)
                inserted_ids.append(product.id)
                logger.debug(
                    f"更新商品[product]数据成功, id={product.id}, product_id={product.product_id}, source={product.source}"
                )
            else:
                logger.info(f"insert product data: {item}")
                stmt = insert(Product).values(item)
                result = session.execute(stmt)
                session.commit()
                insert_id = result.inserted_primary_key[0] if result.inserted_primary_key else None
                if insert_id:
                    inserted_ids.append(insert_id)
                    product = session.execute(select(Product).filter(Product.id == insert_id)).scalars().one_or_none()
                    logger.debug(
                        f"插入商品[product]数据成功, id={product.id}, product_id={product.product_id}, source={product.source}"
                    )
        end_time = time.time()  # 结束计时
        logger.debug(f"保存商品[product]数据: {product_id=}, {source=}，耗时 {end_time - start_time:.2f} 秒")
        return inserted_ids if inserted_ids else None


def save_product_detail_data(data: dict | list[dict]):
    """
    保存数据为json 和数据库
    """
    start_time = time.time()
    if isinstance(data, dict):
        data = [data]
    data: list = field_filter(ProductDetail, data)
    inserted_ids = []
    with Session(engine) as session:
        for item in data:
            product_id = item.get("product_id")
            source = item.get("source")

            # 获取外键Product.id
            result = session.execute(
                select(Product.id).filter(
                    Product.product_id == product_id,
                    Product.source == source,
                )
            )
            product_inner_id = result.scalar_one_or_none()

            if not product_inner_id:
                logger.error(f"未找到对应的Product, product_id={product_id}, source={source}")
                continue

            # 将数据的id
            item["id"] = product_inner_id

            product_detail = (
                session.execute(
                    select(ProductDetail).filter(
                        ProductDetail.product_id == product_id,
                        ProductDetail.source == source,
                    )
                )
                .scalars()
                .one_or_none()
            )
            if product_detail:
                for key, value in item.items():
                    setattr(product_detail, key, value)
                session.add(product_detail)
                session.commit()
                session.refresh(product_detail)
                inserted_ids.append(product_detail.id)
                logger.debug(
                    f"更新商品详情[product_detail]数据成功, id={product_detail.id}, product_id={product_detail.product_id}, source={product_detail.source}"
                )
            else:
                logger.info(f"insert product_detail data: {item}")
                stmt = insert(ProductDetail).values(item)
                result = session.execute(stmt)
                session.commit()
                insert_id = result.inserted_primary_key[0] if result.inserted_primary_key else None
                if insert_id:
                    inserted_ids.append(insert_id)
                    product_detail = (
                        session.execute(select(ProductDetail).filter(ProductDetail.id == insert_id))
                        .scalars()
                        .one_or_none()
                    )
                    logger.debug(
                        f"插入商品详情[product_detail]数据成功, id={product_detail.id}, product_id={product_detail.product_id}, source={product_detail.source}"
                    )
        end_time = time.time()  # 结束计时
        logger.debug(f"保存商品详情[product_detail]数据: {product_id=}, {source=}，耗时 {end_time - start_time:.2f} 秒")
        return inserted_ids if inserted_ids else None


def save_review_data_bulk(data: dict | list[dict]):
    """
    批量保存数据到数据库
    """
    start_time = time.time()

    if isinstance(data, dict):
        data = [data]

    data: list = field_filter(ProductReview, data)  # 假设field_filter是一个预处理数据的函数

    with Session(engine) as session:
        # 准备要插入或更新的对象列表
        reviews_to_persist = []
        existing_reviews = {}  # 用于缓存已存在的记录，避免多次查询

        for item in data:
            review_id = item.get("review_id")
            source = item.get("source")
            if review_id is None:
                logger.error("review_id is None")
                continue

            # 尝试从缓存中获取已存在的记录，减少查询次数
            if (review_id, source) not in existing_reviews:
                existing_review = (
                    session.query(ProductReview)
                    .filter(ProductReview.review_id == review_id, ProductReview.source == source)
                    .one_or_none()
                )
                existing_reviews[(review_id, source)] = existing_review

            review = existing_reviews[(review_id, source)]

            if review:
                # 更新现有记录
                for key, value in item.items():
                    setattr(review, key, value)
                reviews_to_persist.append(review)
            else:
                # 准备新记录用于插入
                reviews_to_persist.append(ProductReview(**item))

        try:
            # 执行批量插入/更新
            # log.debug(reviews_to_persist)
            session.bulk_save_objects(reviews_to_persist)
            session.flush()  # 需要flush以生成主键（如果适用）
            logger.debug(f"批量插入评论[review]数据成功, 一共{len(reviews_to_persist)}条记录")
        except IntegrityError as e:
            # 处理可能的唯一性约束冲突等错误
            session.rollback()
            logger.error(f"数据批量插入失败: {e}")
            return None

        # 提交事务
        session.commit()

        # 如果需要返回插入的ID，可以通过遍历reviews_to_persist并检查id来实现，但需注意这可能会有性能影响
        inserted_ids = [review.review_id for review in reviews_to_persist if hasattr(review, "review_id")]

        logger.debug(f"批量操作完成，共处理{len(inserted_ids)}条记录")
        end_time = time.time()  # 结束计时
        logger.debug(f"保存评论[review]数据完成，耗时 {end_time - start_time:.2f} 秒")

        return inserted_ids or None


async def save_review_data_async_old(data: dict | list[dict]):
    """
    保存数据为json 和数据库
    主语
    """
    start_time = time.time()  # 开始计时

    if isinstance(data, dict):
        data = [data]

    data: list = field_filter(ProductReview, data)

    async with AsyncSession(async_engine) as session:
        inserted_ids = []
        for item in data:
            review_id = item.get("review_id")
            source = item.get("source")
            ...
            if review_id is None:
                logger.error("review_id is None")
                continue

            result = await session.execute(
                select(ProductReview).filter(ProductReview.review_id == review_id, ProductReview.source == source)
            )
            review = result.scalars().one_or_none()

            if review:
                for key, value in item.items():
                    setattr(review, key, value)
                session.add(review)
                await session.commit()
                await session.refresh(review)
                logger.debug(
                    f"更新评论[review]数据成功, id={review.id},review_id={review.review_id} , product_id={review.product_id}, source={review.source}"
                )
                if review.product_id != item.get("product_id"):
                    logger.error(f"product_id 不一致, {review.product_id} != {item.get('product_id')}")

                inserted_ids.append(review.id)
            else:
                stmt = insert(ProductReview).values(item)
                result = await session.execute(stmt)
                await session.commit()

                insert_id = result.inserted_primary_key[0] if result.inserted_primary_key else None
                if insert_id:
                    inserted_ids.append(insert_id)
                    result = await session.execute(select(ProductReview).filter(ProductReview.id == insert_id))
                    review = result.scalars().one_or_none()

                    logger.debug(
                        f"插入评论[review]数据成功, id={review.id}, product_id={review.product_id}, source={review.source}"
                    )

        end_time = time.time()  # 结束计时
        logger.debug(f"保存评论[review]数据完成，耗时 {end_time - start_time:.2f} 秒")
        return inserted_ids if inserted_ids else None


async def save_review_data_async(data: dict | list[dict]):
    """
    保存数据为json 和数据库
    """
    start_time = time.time()  # 开始计时

    if isinstance(data, dict):
        data = [data]

    data: list[dict] = field_filter(ProductReview, data)

    async with AsyncSession(async_engine) as session:
        inserted_ids = []
        to_insert = []
        to_update = []

        for item in data:
            review_id = item.get("review_id")
            product_id = item.get("product_id")
            source = item.get("source")

            if review_id is None:
                logger.error("review_id is None")
                continue

            result = await session.execute(
                select(ProductReview).filter(
                    ProductReview.review_id == review_id,
                    ProductReview.product_id == product_id,
                    ProductReview.source == source,
                )
            )
            review = result.scalars().one_or_none()

            if review:
                # 如果存在，更新
                update_data = {key: value for key, value in item.items()}
                # 携带主键
                update_data.update({"id": review.id})
                to_update.append(update_data)
            else:
                # 如果不存在，插入
                to_insert.append(item)

        # 批量插入
        if to_insert:
            stmt = insert(ProductReview).values(to_insert)
            result = await session.execute(stmt)
            await session.commit()
            logger.debug(f"批量插入评论[review]数据成功, 一共{len(to_insert)}条记录")
            for insert_id in result.inserted_primary_key:
                if insert_id:
                    inserted_ids.append(insert_id)

        # 批量更新
        if to_update:
            logger.debug(f"待更新{len(to_update)}数据")
            kwargs = {key: bindparam(key) for key in to_update[0].keys()}
            stmt = (
                update(ProductReview)
                .where(ProductReview.review_id == bindparam("review_id"), ProductReview.source == bindparam("source"))
                .values(**kwargs)
                .execution_options(synchronize_session=False)
            )

            await session.execute(stmt, to_update)
            await session.commit()
            logger.debug(f"批量更新评论[review]数据成功, 一共{len(to_update)}条记录")

        end_time = time.time()  # 结束计时
        logger.debug(f"保存评论[review]数据完成 {len(data)}条数据，耗时 {end_time - start_time:.2f} 秒")
        return inserted_ids if inserted_ids else None


async def save_product_data_async(data: dict | list[dict]) -> str | None:
    """
    保存数据为json 和数据库
    """
    start_time = time.time()
    if isinstance(data, dict):
        data = [data]
    data: list = field_filter(Product, data)
    inserted_ids = []
    async with AsyncSession(async_engine) as session:
        for item in data:
            product_id = item.get("product_id")
            source = item.get("source")

            result = await session.execute(
                select(Product).filter(
                    Product.product_id == product_id,
                    Product.source == source,
                )
            )
            product = result.scalars().one_or_none()

            if product:
                logger.debug(
                    f"更新前的product数据: {product.product_id=}, {product.primary_sku_id=}, {product.source=}, {product.product_name=}, {product.product_url=}, {product.category=}, {product.gender=}, {product.released_at=}"
                )

                for key, value in item.items():
                    setattr(product, key, value)
                session.add(product)
                await session.commit()
                await session.refresh(product)
                logger.debug(
                    f"更新后的product数据: {product.product_id=}, {product.primary_sku_id=}, {product.source=}, {product.product_name=}, {product.product_url=}, {product.category=}, {product.gender=}, {product.released_at=}"
                )
                logger.debug(f"插入的product数据: {item}")
                inserted_ids.append(product.id)
                logger.debug(
                    f"更新商品[product]数据成功, id={product.id}, product_id={product.product_id}, source={product.source}"
                )
            else:
                logger.info(f"insert product data: {item}")
                stmt = insert(Product).values(item)
                result = await session.execute(stmt)
                await session.commit()
                insert_id = result.inserted_primary_key[0] if result.inserted_primary_key else None
                if insert_id:
                    inserted_ids.append(insert_id)
                    result = await session.execute(select(Product).filter(Product.id == insert_id))
                    product = result.scalars().one_or_none()
                    logger.debug(
                        f"插入商品[product]数据成功, id={product.id}, product_id={product.product_id}, source={product.source}"
                    )
        end_time = time.time()  # 结束计时
        logger.debug(f"保存商品[product]数据: {product_id=}, {source=},耗时 {end_time - start_time:.2f} 秒")
        return inserted_ids if inserted_ids else None


async def save_sku_data_async(data: dict | list[dict]) -> list | None:
    """
    保存数据为json 和数据库
    """
    start_time = time.time()
    if isinstance(data, dict):
        data = [data]
    data: list = field_filter(ProductSKU, data)
    inserted_ids = []
    async with AsyncSession(async_engine) as session:
        for item in data:
            sku_id = item.get("sku_id")
            source = item.get("source")
            product_id = item.get("product_id")

            result = await session.execute(
                select(ProductSKU).filter(
                    ProductSKU.sku_id == sku_id, ProductSKU.source == source, ProductSKU.product_id == product_id
                )
            )
            sku = result.scalars().one_or_none()
            if sku:
                logger.debug(
                    f"更新前的SKU数据: {sku.product_id=}, {sku.sku_id=}, {sku.source=}, {sku.color=}, {sku.product_url=}, {sku.outer_model_image_urls=}, {sku.outer_image_url=}"
                )
                for key, value in item.items():
                    setattr(sku, key, value)
                session.add(sku)
                await session.commit()
                await session.refresh(sku)
                logger.debug(
                    f"更新后的SKU数据: {sku.product_id=}, {sku.sku_id=}, {sku.source=}, {sku.color=}, {sku.product_url=}, {sku.outer_model_image_urls=}, {sku.outer_image_url=}"
                )
                logger.debug(f"插入的product数据: {item}")
                logger.debug(
                    f"更新子款[SKU] 数据成功, id={sku.id}, sku_id={sku.sku_id}, product_id={sku.product_id}, source={sku.source}"
                )
                inserted_ids.append(sku.id)
            else:
                stmt = insert(ProductSKU).values(item)
                result = await session.execute(stmt)
                await session.commit()
                insert_id = result.inserted_primary_key[0] if result.inserted_primary_key else None
                if insert_id:
                    inserted_ids.append(insert_id)
                    result = await session.execute(select(ProductSKU).filter(ProductSKU.id == insert_id))
                    sku = result.scalars().one_or_none()
                    logger.debug(
                        f"插入子款[SKU] 数据成功, id={sku.id}, sku_id={sku.sku_id}, product_id={sku.product_id}, source={sku.source}"
                    )
        end_time = time.time()  # 结束计时
        logger.debug(f"保存子款[sku]数据完成，耗时 {end_time - start_time:.2f} 秒")
        return inserted_ids if inserted_ids else None


async def save_product_detail_data_async(data: dict | list[dict]) -> str | None:
    """
    保存数据为json 和数据库
    """
    start_time = time.time()
    if isinstance(data, dict):
        data = [data]
    data: list = field_filter(ProductDetail, data)
    inserted_ids = []
    async with AsyncSession(async_engine) as session:
        for item in data:
            product_id = item.get("product_id")
            source = item.get("source")

            # 获取外键Product.id
            result = await session.execute(
                select(Product.id).filter(
                    Product.product_id == product_id,
                    Product.source == source,
                )
            )
            product = result.scalar_one_or_none()

            if not product:
                logger.error(f"未找到对应的Product, product_id={product_id}, source={source}")
                continue

            # 将商品的内部id
            item["id"] = product

            result = await session.execute(
                select(ProductDetail).filter(
                    ProductDetail.product_id == product_id,
                    ProductDetail.source == source,
                )
            )
            product_detail = result.scalars().one_or_none()

            if product_detail:
                logger.debug(
                    f"更新前的product_detail数据: {product_detail.product_id=}, {product_detail.main_category=}, {product_detail.sub_category=}, {product_detail.source=}"
                )
                for key, value in item.items():
                    setattr(product_detail, key, value)
                session.add(product_detail)
                await session.commit()
                await session.refresh(product_detail)
                logger.debug(
                    f"更新后的product_detail数据: {product_detail.product_id=}, {product_detail.main_category=}, {product_detail.sub_category=}, {product_detail.source=}"
                )
                logger.debug(f"插入的product_detail数据: {item}")

                inserted_ids.append(product_detail.id)
                logger.debug(
                    f"更新商品详情[product_detail]数据成功, id={product_detail.id}, product_id={product_detail.product_id}, source={product_detail.source}"
                )
            else:
                logger.info(f"insert product_detail data: {item}")
                stmt = insert(ProductDetail).values(item)
                result = await session.execute(stmt)
                await session.commit()
                insert_id = result.inserted_primary_key[0] if result.inserted_primary_key else None
                if insert_id:
                    inserted_ids.append(insert_id)
                    result = await session.execute(select(ProductDetail).filter(ProductDetail.id == insert_id))
                    product_detail = result.scalars().one_or_none()
                    logger.debug(
                        f"插入商品详情[product_detail]数据成功, id={product_detail.id}, product_id={product_detail.product_id}, source={product_detail.source}"
                    )
        end_time = time.time()  # 结束计时
        logger.debug(f"保存商品详情[product_detail]数据: {product_id=}, {source=},耗时 {end_time - start_time:.2f} 秒")
        return inserted_ids if inserted_ids else None


if __name__ == "__main__":
    logger.debug("test")
    logger.error("error")
    logger.info("info")
    logger.warning("warning")
    # print(save_product_data({"product_id": 12, "name": "test", "source": "gap2"}))
    # print(save_review_data({"review_id": 3, "product_name": "test2", "source": "gap", "product_id": 1}))
    timestamp = 1715911559159 / 1000  # 转换为秒
    time_string = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    print(time_string)
    datetime_obj = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
    print(datetime_obj)

    async def run():
        # result = await save_sku_data_async(
        #     {
        #         "product_id": 9999991,
        #         "sku_id": 5,
        #         "product_name": "test3",
        #         "source": "other",
        #         "released_at": time_string,
        #         "color": "你好",
        #         "attributes": {"test": 12},
        #     }
        # ),
        result = (
            await save_product_data_async(
                {
                    "product_id": 9999991,
                    "sku_id": 5,
                    "product_name": "test3",
                    "source": "other",
                    "released_at": time_string,
                    "color": "你好",
                    "attributes": {"test": 12},
                }
            ),
        )
        result2 = (
            await save_product_detail_data_async(
                {
                    "product_id": 9999991,
                    "sku_id": 5,
                    "product_name": "test3",
                    "source": "other",
                    "fit": "44",
                    "softness": "44",
                    "released_at": time_string,
                    "color": "你好",
                    "attributes": {"test": 12},
                }
            ),
        )
        logger.debug(result)
        return result, result2

    result = asyncio.run(run())
    print(result)

    # print(
    #     "已插入数据: ",
    #     save_review_data_bulk(
    #         [
    #             {
    #                 "product_id": 999999,
    #                 "review_id": "test-001",
    #                 "sku_id": 5,
    #                 "product_name": "test3",
    #                 "source": "other",
    #                 "attributes": {"test": 12},
    #             },
    #             {
    #                 "product_id": 999999,
    #                 "review_id": "test-002",
    #                 "sku_id": 5,
    #                 "product_name": "test3",
    #                 "source": "other",
    #                 "attributes": {"test": 12},
    #             },
    #             {
    #                 "product_id": 999999,
    #                 "review_id": "test-003",
    #                 "sku_id": 5,
    #                 "product_name": "test3",
    #                 "source": "other",
    #                 "attributes": {"test": 12},
    #             },
    #             {
    #                 "product_id": 999999,
    #                 "review_id": "test-004",
    #                 "sku_id": 5,
    #                 "product_name": "test3",
    #                 "source": "other",
    #                 "attributes": {"test": 12},
    #             },
    #         ]
    #     ),
    # )
