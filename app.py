import re

from flask import Flask, render_template, request
from database import Select_sidebar, Selection_dishes_search, Selection_dishes_tags, Update_insert_cart, Select_indents
from database import Update_delete_cart, Authorization_verification, Update_assortment_insert, Select_assortment, Update_assortment_delete

previous_search_result = []

app = Flask(__name__)


@app.route("/Search2/Authorization/OwnerMode", methods=["GET", "POST"])
def Owner_mode():
    Colunm_list = ["Item_Number", "Supply_number", "Clients_number", "Product_type_number",
                   "Product_material_number", "Dishes_stock_number", "Price", "Size",
                   "Indent_number", "Provider_number"]
    top_menu_activity = ["inactive", "active", "inactive"]

    if request.method == "POST":
        if re.match(".+button_delete.+", str(request.form)):
            Update_assortment_delete(request.form)
        if re.match(".+button_insert.+", str(request.form)):
            Update_assortment_insert(request.form)
        if re.match(".+button_logout.+", str(request.form)):
            return render_template("dashboard_2.jinja", top_menu_activity=top_menu_activity)

    return render_template("dashboard_2.jinja", top_menu_activity=top_menu_activity, OwnerMode=1,
                           Assortment=Select_assortment(), Colunm_list=Colunm_list)


# @app.post("/Search2/Authorization")
# def Users_post():
# action="/Search2/Authorization/<login>"
already_login = False


@app.route("/Search2/Authorization", methods=["GET", "POST"])
def hello_world():
    global already_login
    usrnm = ""
    email = ""
    psw =""
    Colunm_list = ["Item_Number", "Supply_number", "Clients_number", "Product_type_number",
                   "Product_material_number", "Dishes_stock_number", "Price", "Size",
                   "Indent_number", "Provider_number"]
    top_menu_activity = ["inactive", "active", "inactive"]
    if request.method == "POST":
        if "Login" in request.form:
            usrnm = request.form.get("usrnm")
            email = request.form.get("email")
            psw = request.form.get("psw")
            # return f'{usrnm}____{email}____{psw}'
    link = "/Search2/Authorization/OwnerMode"
    if request.method == "POST":
        if re.match(".+button_logout.+", str(request.form)):
            already_login = False
            return render_template("dashboard_2.jinja", top_menu_activity=top_menu_activity)

    if (usrnm == "FFFF F.F." and email == "FFFFFF@gmail.com" and psw == "80000000000") or already_login:
        already_login = True
        if request.method == "POST":
            if re.match(".+button_delete.+", str(request.form)):
                Update_assortment_delete(request.form)
            if re.match(".+button_insert.+", str(request.form)):
                Update_assortment_insert(request.form)

        return render_template("dashboard_2.jinja", top_menu_activity=top_menu_activity, OwnerMode=1,
                               Assortment=Select_assortment(), Colunm_list=Colunm_list, link=link)

    return render_template("dashboard_2.jinja", Authorization=1, top_menu_activity=top_menu_activity, link="")


# @app.route("/Search2/Authorization", methods=["GET", "POST"])
# def Authorization():
#     link = "/Search2/Authorization/<login>"
#     top_menu_activity = ["inactive", "active", "inactive"]
#     return render_template("dashboard_2.jinja", Authorization=1, top_menu_activity=top_menu_activity)


@app.route("/Search2/Cart", methods=["GET", "POST"])
def Cart():
    top_menu_activity = ["inactive", "inactive", "active"]
    sidebar = Select_sidebar()
    if request.method == "POST":
        if re.match(".+button_buy_[1-9]+.+", str(request.form)):
            str_ = re.search("[1-9]+", str(request.form))
            Update_delete_cart(str_[0])

    return render_template("dashboard_2.jinja",
                           dishes_search=Select_indents(), button_add_delete="Удалить из корзины",
                           sidebar=sidebar, top_menu_activity=top_menu_activity)


@app.route("/Search2")
def Search2():
    top_menu_activity = ["active", "inactive", "inactive"]
    sidebar = Select_sidebar()
    return render_template("dashboard_2.jinja", sidebar=sidebar, button_add_delete="Добавить в корзину",
                           top_menu_activity=top_menu_activity)


@app.route("/Search2", methods=["POST", "GET", "PUT"])
def Search_requests2():
    top_menu_activity = ["active", "inactive", "inactive"]
    sidebar = Select_sidebar()
    tags_list = []
    global previous_search_result

    if request.method == "POST":
        if re.match(".+button_buy_[1-9]+.+", str(request.form)):
            str_ = re.search("[1-9]+", str(request.form))
            Update_insert_cart(str_[0])
            return render_template("dashboard_2.jinja", sidebar=sidebar, button_add_delete="Добавить в корзину",
                                   top_menu_activity=top_menu_activity, dishes_search=previous_search_result)

    if request.method == "POST":
        if "button_tags" in request.form:
            for item_ in request.form:
                if item_ != "button_tags":
                    tags_list.append(item_)

            previous_search_result = Selection_dishes_tags(tags_list, sidebar)
            return render_template("dashboard_2.jinja",
                                   dishes_search=Selection_dishes_tags(tags_list, sidebar),
                                   sidebar=sidebar, top_menu_activity=top_menu_activity,
                                   button_add_delete="Добавить в корзину")

    if request.method == "POST":
        if request.form["Search2"]:
            previous_search_result = Selection_dishes_search(request.form["Search2"])
            return render_template("dashboard_2.jinja",
                                   dishes_search=Selection_dishes_search(request.form["Search2"]),
                                   sidebar=sidebar, top_menu_activity=top_menu_activity,
                                   button_add_delete="Добавить в корзину")

    return render_template("dashboard_2.jinja", sidebar=sidebar, top_menu_activity=top_menu_activity,
                           button_add_delete="Добавить в корзину")
