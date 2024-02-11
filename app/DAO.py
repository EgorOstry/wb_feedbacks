from database import engine, Session

# Создание таблицы ProductsMapping, если она еще не создана
# ProductsMapping.__table__.create(bind=engine, checkfirst=True)

# Функция для добавления тестовой записи в таблицу ProductsMapping
def add_test_product_mapping():
    # Создаем новый объект сессии
    session = Session()

    # Проверяем, существует ли уже запись с таким marketplace_id и external_code
    exists = session.query(ProductsMapping.id).filter_by(marketplace_id=1, external_code=17631627).scalar() is not None
    if not exists:
        # Создаем тестовую запись
        test_mapping = ProductsMapping(
            marketplace_id=1,  # ID для маркетплейса Wildberries
            internal_code=12345678,  # Пример внутреннего артикула
            external_code=17631627  # Пример артикула с маркетплейса Wildberries
        )
        # Добавляем запись в сессию и коммитим транзакцию
        session.add(test_mapping)
        session.commit()
        print(f"Добавлена тестовая запись с internal_code {test_mapping.internal_code} и external_code {test_mapping.external_code}")
    else:
        print("Тестовая запись уже существует.")

    # Закрываем сессию
    session.close()

# Вызов функции для добавления тестовой записи
add_test_product_mapping()
