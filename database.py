import re
from datetime import datetime, date, time

import sqlalchemy
from sqlalchemy import create_engine, inspect, select, delete
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import or_, and_, not_, desc

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


def func_chunk(lst, n):
    for x in range(0, len(lst), n):
        e_c = lst[x : n + x]

        if len(e_c) < n:
            e_c = e_c + [None for y in range(n - len(e_c))]
        yield e_c


def Select_assortment():
    assortment = select(dishes).select_from(dishes).where(dishes.c.Clients_number == 1)
    select_assortment_list = Select_items_as_list(assortment)
    final_select = func_chunk(select_assortment_list, 10)

    return final_select


def Update_assortment_delete(request):
    dsh_number = request["Item_Number_delete"]
    ass = delete(dishes).where(dishes.c.Item_Number == int(dsh_number))

    with engine.connect() as conn_:
        res = conn_.execute(ass)


def Update_assortment_insert(request):

    dsh = dishes.insert().values(
        # Item_Number=request["Item_Number_insert"],
        # Supply_number=request["Supply_number_insert"],
        # Clients_number=request["Clients_number_insert"],
        # Product_type_number=request["Product_type_number_insert"],
        # Product_material_number=request["Product_material_number_insert"],
        # Dishes_stock_number=request["Dishes_stock_number_insert"],
        # Price=request["Price_insert"],
        # Size=request["Size_insert"],
        # Indent_number=request["Indent_number_insert"],
        # Provider_number=request["Provider_number_insert"]
        Item_Number=int(request["Item_Number_insert"]),
        Supply_number=int(request["Supply_number_insert"]),
        Clients_number=int(request["Clients_number_insert"]),
        Product_type_number=int(request["Product_type_number_insert"]),
        Product_material_number=int(request["Product_material_number_insert"]),
        Dishes_stock_number=int(request["Dishes_stock_number_insert"]),
        Price=int(request["Price_insert"]),
        Size=int(request["Size_insert"]),
        Indent_number=int(request["Indent_number_insert"]),
        Provider_number=int(request["Provider_number_insert"])
        # Item_Number=7,
        # Supply_number=3,
        # Clients_number=1,
        # Product_type_number=3,
        # Dishes_stock_number=2222,
        # Price=890,
        # Size=200,
        # Indent_number=1,
        # Provider_number=2
    )

    with engine.connect() as conn_:
        res = conn_.execute(dsh)


def Authorization_verification(search_login):
    owner_verification = select(client.c.Full_name).select_from(client).\
            where(
                client.c.Contact_mail == search_login
            )
    select_authorization_list = []
    with engine.connect() as conn:
        result = conn.execute(owner_verification)
        for tuple_ in result:
            select_authorization_list.append(tuple_)
    return select_authorization_list


def Select_indents():
    select_indent = select(indent.c.Indent_number, indent.c.Indent_price, indent.c.Product_type,
                           indent.c.Product_material).\
        select_from(indent).\
        where(
        indent.c.Clients_number == 4
    )

    select_indent_list = []
    with engine.connect() as conn:
        result = conn.execute(select_indent)
        for tuple_ in result:
            select_indent_list.append(tuple_)
    return select_indent_list


def Update_delete_cart(delete_dishes):
    ins = delete(indent).where(
        indent.c.Indent_number == delete_dishes
    )

    with engine.connect() as conn_:
        res = conn_.execute(ins)


def Update_insert_cart(add_dishes):
    selected_item = select(dishes.c.Clients_number, dishes.c.Price, type.c.Title, material.c.Material_name).\
        select_from(dishes.join(type).join(material)).\
        where(
            dishes.c.Item_Number == add_dishes
    )
    selected_item_list = Select_items_as_list(selected_item)

    selected_max_number = select(indent.c.Indent_number).\
        order_by(desc(indent.c.Indent_number)).limit(1)
    selected_max_number_list = Select_items_as_list(selected_max_number)
    max_indent_number = int(selected_max_number_list[0]) + 1

    ins = indent.insert().values(
        Indent_number=max_indent_number,
        Clients_number=4,
        Indent_date=datetime.date(datetime.now()),
        Indent_price=selected_item_list[1],
        Quantity_of_indent=1,
        Product_type=selected_item_list[2],
        Product_material=selected_item_list[3]
    )
    with engine.connect() as conn_:
        res = conn_.execute(ins)


def Selection_dishes_tags(tags_request, sidebar):
    provider_list = []
    material_list = []
    type_list = []
    for key_ in sidebar:
        for item_sidebar in sidebar[key_]:
            if item_sidebar in tags_request:
                if key_ == "provider":
                    provider_list.append(item_sidebar)
                if key_ == "material":
                    material_list.append(item_sidebar)
                if key_ == "type":
                    type_list.append(item_sidebar)

    if len(provider_list) == 0:
        S_p = select(provider.c.Company_name)
        provider_list = Select_items_as_list(S_p)

    if len(material_list) == 0:
        S_m = select(material.c.Material_name)
        material_list = Select_items_as_list(S_m)

    if len(type_list) == 0:
        S_t = select(type.c.Title)
        type_list = Select_items_as_list(S_t)

    Select_dishes_tags = select(dishes.c.Item_Number, type.c.Title, material.c.Material_name, provider.c.Company_name).\
        select_from(dishes.join(type).join(material).join(provider)).\
        where(
            and_(
                provider.c.Company_name.in_(provider_list),
                type.c.Title.in_(type_list),
                material.c.Material_name.in_(material_list)
            )
    )

    dishes_list = []
    with engine.connect() as conn:
        result = conn.execute(Select_dishes_tags)
        for tuple_ in result:
            dishes_list.append(tuple_)
    return dishes_list


def Selection_dishes_search(search_request):
    search_material = re.search("ceramics|porcelain|glass|plastic", search_request)
    search_type = re.search("cup|plate|wineglass", search_request)
    search_dishes = re.search("[1-9]+", search_request)

    if search_material is not None:
        str_material = str(search_material[0])
    else:
        str_material = "%%"
    if search_type is not None:
        str_type = str(search_type[0])
    else:
        str_type = "%%"
    if search_dishes is not None:
        str_dishes = str(search_dishes[0])
    else:
        str_dishes = "%%"

    Select_dsh = select(dishes.c.Item_Number, type.c.Title, material.c.Material_name).\
        select_from(dishes.join(type).join(material)).\
        where(
            and_(
                type.c.Title.like(str_type),
                material.c.Material_name.like(str_material),
                dishes.c.Item_Number.like(str_dishes)
            )
    )
    dishes_list = []
    with engine.connect() as conn:
        result = conn.execute(Select_dsh)
        for tuple_ in result:
            dishes_list.append(tuple_)
    return dishes_list


Selection_dishes_search("cup")


def Select_sidebar():
    select_sidebar_type = select(type.c.Title)
    select_sidebar_material = select(material.c.Material_name)
    select_sidebar_provider = select(provider.c.Company_name)
    sidebar_dict = {"type": Select_items_as_list(select_sidebar_type),
                    "material": Select_items_as_list(select_sidebar_material),
                    "provider": Select_items_as_list(select_sidebar_provider)}

    return sidebar_dict


def Select_items_as_list(select_result):
    items_list = []
    with engine.connect() as conn_:
        result_ = conn_.execute(select_result)
        for tuple_ in result_:
            items_list = items_list + (list(tuple_))
        return items_list


Select_sidebar()
Select_indents()
