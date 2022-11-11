import sqlalchemy
from sqlalchemy import create_engine, inspect, select
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import or_, and_, not_

engine = create_engine("mysql+pymysql://root:Rom_544!@localhost:3306/my_db_dsh")
engine.connect()
Inspector = inspect(engine)

print(engine)
print(Inspector.get_table_names())
print(Inspector.get_columns("indent"))

metadata = MetaData()
metadata.bind = engine
print(metadata.is_bound())
print(metadata.tables)
metadata.reflect()
for t in metadata.tables:
    print(metadata.tables[t])

indent = Table("indent", metadata)
client = Table("client", metadata)
dishes = Table("dishes", metadata)
material = Table("material", metadata)
material_of_manufactured_products = Table("material_of_manufactured_products", metadata)
place_of_storage_of_dishes = Table("place_of_storage_of_dishes", metadata)
place_of_storage_of_raw_materials = Table("place_of_storage_of_raw_materials", metadata)
production_batch = Table("production_batch", metadata)
production_material = Table("production_material", metadata)
provider = Table("provider", metadata)
supply = Table("provider", metadata)
type = Table("type", metadata)
type_of_manufactured_products = Table("type_of_manufactured_products", metadata)


s = indent.select()
with engine.connect() as conn:
    result = conn.execute(s)
    for row in result:
        print(row)


def Select_dishes(search_request):
    print("***************************")
    # Select_dsh = select(dishes.c.Product_type_number).where(
    #     dishes.c.Product_type_number == search_request
    # )
    # Select_dsh = select(type.c.Title).select_from(type.join(dishes)).where(
    #     type.c.Title == search_request
    # )
    Select_dsh = select(dishes.c.Item_Number, type.c.Title, material.c.Material_name).\
        select_from(dishes.join(type).join(material)).\
        where(
            or_(
                type.c.Title == search_request,
                material.c.Material_name == search_request,
                dishes.c.Item_Number == search_request
            )
    )
    with engine.connect() as conn:
        # return conn.execute(Select_dsh)
        # print(conn.execute(Select_dsh))
        result = conn.execute(Select_dsh)
        search_word = ""
        for row in result:
            for word in row:
                search_word = search_word + str(word)
            print(search_word)
            search_word = ""


Select_dishes("cup")
# , type.c.Title, , provider.c.Company_name


def Select_sidebar():
    select_sidebar_type = select(type.c.Title)
    select_sidebar_material = select(material.c.Material_name)
    select_sidebar_provider = select(provider.c.Company_name)

    sidebar_list = [Select_items_as_list(select_sidebar_type),
                    Select_items_as_list(select_sidebar_material),
                    Select_items_as_list(select_sidebar_provider)]

    return sidebar_list


def Select_items_as_list(select_result):
    items_list = []
    with engine.connect() as conn_:
        result_ = conn_.execute(select_result)
        for tuple_ in result_:
            items_list = items_list + (list(tuple_))
        return items_list


Select_sidebar()
