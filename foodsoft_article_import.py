import csv

import base
import foodsoft_article
# import foodsoft # not needed anymore, if we use foodsoft_connector from given session

def remove_articles_to_ignore(articles):
    return [x for x in articles if not x.ignore]

def get_duplicates(article, articles):
    # get list of articles of the same name, or differing only in upper-/lowercase or whitespaces
    return [a for a in articles if a.name.casefold().replace(" ", "") == article.name.casefold().replace(" ", "")]

def rename_duplicates(articles):
    # Foodsoft requires articles to have a unique name. It is also useful if they can clearly by distinguished e.g. on printed order lists.

    # Check if articles of the same name can be distinguished by their unit, and rename them if so
    articles_to_rename = {}
    for article in articles:
        articles_of_this_name = get_duplicates(article, articles)
        if len(articles_of_this_name) > 1:
            if article.orig_unit:
                articles_of_this_unit = [a for a in articles_of_this_name if a.orig_unit.casefold().replace(" ", "") == article.orig_unit.casefold().replace(" ", "")]
                if len(articles_of_this_unit) != len(articles_of_this_name):
                    articles_to_rename[article] = article.name + foodsoft_article.suffix(article.orig_unit)
    for article in articles_to_rename:
        article.name = articles_to_rename[article]

    # For articles of the same name and unit, check if they can be distinguished by their manufacturer, and rename them if so
    articles_to_rename = {}
    for article in articles:
        articles_of_this_name = get_duplicates(article, articles)
        if len(articles_of_this_name) > 1:
            if article.manufacturer:
                articles_of_this_manufacturer = [a for a in articles_of_this_name if a.manufacturer.casefold().replace(" ", "") == article.manufacturer.casefold().replace(" ", "")]
                if len(articles_of_this_manufacturer) != len(articles_of_this_name):
                    articles_to_rename[article] = article.name + foodsoft_article.suffix(article.manufacturer, "manufacturer")
    for article in articles_to_rename:
        article.name = articles_to_rename[article]
    
    # For articles of the same name and unit which can't be distinguished by their manufacturer, check if they can be distinguished by their origin, and rename them if so
    articles_to_rename = {}
    for article in articles:
        articles_of_this_name = get_duplicates(article, articles)
        if len(articles_of_this_name) > 1:
            if article.origin:
                articles_of_this_origin = [a for a in articles_of_this_name if a.origin.casefold().replace(" ", "") == article.origin.casefold().replace(" ", "")]
                if len(articles_of_this_origin) != len(articles_of_this_name):
                    articles_to_rename[article] = article.name + foodsoft_article.suffix(article.origin, "origin")
    for article in articles_to_rename:
        article.name = articles_to_rename[article]
    
    # For articles which still couldn't be distinguished, add numbers (1), (2), etc.
    articles_to_rename = {}
    for article in articles:
        articles_of_this_name = get_duplicates(article, articles)
        if len(articles_of_this_name) > 1:
            articles_to_rename[article] = article.name + foodsoft_article.suffix(articles_of_this_name.index(article) + 1)
    for article in articles_to_rename:
        article.name = articles_to_rename[article]

    return articles

def compare_string(article, article_from_last_run, article_from_foodsoft, string_type, configuration_config, notifications):
    if string_type not in ["name", "note", "manufacturer", "origin", "unit", "price_net", "vat", "deposit", "unit_quantity"]:
        notifications.append("Invalid string type for article attribute (look in config file?): " + string_type)
    else:
        replace = False
        if article_from_foodsoft and article_from_last_run:
            if getattr(article, string_type) != getattr(article_from_foodsoft, string_type) and getattr(article, string_type) == getattr(article_from_last_run, string_type):
                replace = True
                replaced_string = getattr(article, string_type)
                manual_string = getattr(article_from_foodsoft, string_type)
                if article.order_number not in configuration_config["manual changes"]:
                    configuration_config["manual changes"][article.order_number] = {}
                configuration_config["manual changes"][article.order_number][string_type] = {}
                configuration_config["manual changes"][article.order_number][string_type]["replaced"] = replaced_string
                configuration_config["manual changes"][article.order_number][string_type]["manual"] = manual_string
                notifications.append("Keeping manual change of article " + string_type + ": " + replaced_string + " -> " + manual_string)
        if not replace and article.order_number in configuration_config["manual changes"]:
            manual_changes = configuration_config["manual changes"][article.order_number]
            if string_type in manual_changes:
                if manual_changes[string_type]["replaced"] == getattr(article, string_type):
                    replace = True
                    manual_string = manual_changes[string_type]["manual"]
        if replace:
            setattr(article, string_type, manual_string)
    return article, configuration_config

def compare_manual_changes(foodcoop, supplier, supplier_id, articles, foodsoft_connector=None, notifications=None, compare_name=True, compare_note=True, compare_manufacturer=True, compare_origin=True, compare_unit=True, compare_price=True, compare_vat=False, compare_deposit=False, compare_unit_quantity=False, compare_category=True):
    """
    This is an optional method which checks if article data has been modified manually in Foodsoft after the last CSV was created.
    In case the article data in the source did not change since the last run of the script and the article data from your Foodsoft instance differs, latter is adopted.
    """

    if not notifications:
        notifications = []

    # Extract the configuration for this supplier
    configuration_config = base.read_config(foodcoop=foodcoop, configuration=supplier)
    if "manual changes" not in configuration_config:
        configuration_config["manual changes"] = {}

    # Connect to your Foodsoft instance and download the articles CSV of the supplier
    if foodsoft_connector and supplier_id:
        # fsc = foodsoft.FSConnector(url=foodsoft_url, user=foodsoft_user, password=foodsoft_password)
        csv_from_foodsoft = csv.reader(foodsoft_connector.get_articles_CSV(supplier_id=supplier_id).splitlines(), delimiter=';')
        # fsc.logout()
        articles_from_foodsoft = foodsoft_article.read_articles_from_csv(csv_from_foodsoft)
    else:
        articles_from_foodsoft = []
        notifications.append("ACHTUNG: Abgleichen der manuellen Änderungen in der Foodsoft fehlgeschlagen, da Foodsoft-Connector fehlt!")

    # Get the last CSV created by the script
    last_imported_run_name = base.read_in_config(configuration_config, "last imported run", "")
    last_imported_csv = None
    if last_imported_run_name:
        last_imported_csv, notifications = base.get_file_path(foodcoop=foodcoop, configuration=supplier, run=last_imported_run_name, folder="download", ending=".csv", notifications=notifications)
    if not last_imported_csv:
        notifications.append("No previous CSV found for comparison.")
        articles_from_last_run = []
    else:
        notifications.append("It was assumed '" + last_imported_csv + "' was the last CSV imported into Foodsoft.")
        with open(last_imported_csv, newline='', encoding='utf-8') as csvfile:
            last_csv_opened = csv.reader(csvfile, delimiter=';')
            articles_from_last_run = foodsoft_article.read_articles_from_csv(last_csv_opened)

    # Compare for each article the newly readout data, the data from Foodsoft, and the data from the last run
    for article in articles:
        article_from_foodsoft_list = [a for a in articles_from_foodsoft if a.order_number == article.order_number]
        if article_from_foodsoft_list:
            article_from_foodsoft = article_from_foodsoft_list[0]
        else:
            article_from_foodsoft = None
        article_from_last_run_list = [a for a in articles_from_last_run if a.order_number == article.order_number]
        if article_from_last_run_list:
            article_from_last_run = article_from_last_run_list[0]
        else:
            article_from_last_run = None

        if compare_name:
            article, configuration_config = compare_string(article, article_from_last_run, article_from_foodsoft, "name", configuration_config, notifications)
        if compare_note:
            article, configuration_config = compare_string(article, article_from_last_run, article_from_foodsoft, "note", configuration_config, notifications)
        if compare_manufacturer:
            article, configuration_config = compare_string(article, article_from_last_run, article_from_foodsoft, "manufacturer", configuration_config, notifications)
        if compare_origin:
            article, configuration_config = compare_string(article, article_from_last_run, article_from_foodsoft, "origin", configuration_config, notifications)
        if compare_unit:
            article, configuration_config = compare_string(article, article_from_last_run, article_from_foodsoft, "unit", configuration_config, notifications)
        if compare_price:
            article, configuration_config = compare_string(article, article_from_last_run, article_from_foodsoft, "price_net", configuration_config, notifications)
        if compare_vat:
            article, configuration_config = compare_string(article, article_from_last_run, article_from_foodsoft, "vat", configuration_config, notifications)
        if compare_deposit:
            article, configuration_config = compare_string(article, article_from_last_run, article_from_foodsoft, "deposit", configuration_config, notifications)
        if compare_unit_quantity:
            article, configuration_config = compare_string(article, article_from_last_run, article_from_foodsoft, "unit_quantity", configuration_config, notifications)
        if compare_category:
            manual_category = False
            if article.order_number in configuration_config["manual changes"]:
                if "category" in configuration_config["manual changes"][article.order_number]:
                    article.category = configuration_config["manual changes"][article.order_number]["category"]
                    manual_category = True
            if not manual_category and article_from_foodsoft:
                if not article.order_number in configuration_config["manual changes"]:
                    configuration_config["manual changes"][article.order_number] = {}
                configuration_config["manual changes"][article.order_number]["category"] = article_from_foodsoft.category
                article.category = article_from_foodsoft.category

    base.save_config(foodcoop=foodcoop, configuration=supplier, config=configuration_config)

    return articles, notifications

def validate_string(string, string_type, article, notifications):
    """
    Check if unit, name, and other strings exceed the respective character limit, and shorten them if so
    """
    string = str(string)
    if string_type != "unit" and string_type != "name": # Units and names could also be shortened, but Foodsoft will validate them, so it's not necessary.
        max_length = 255
        abort_string = "..."
        if len(string) > max_length:
            short_length = max_length - len(abort_string)
            shortened_string = string[0:short_length] + abort_string
            message = "Overlong article " + string_type + " (" + str(len(string)) + " characters) of article #" + str(article.order_number) + " (" + str(article.name) + ") registered, shortened to " + str(len(shortened_string)) + " characters."
            notifications.append(message)
            string = shortened_string

    string.replace(';', ',')
    return string, notifications

def get_data_from_articles(articles, notifications):
    """
    Transform instances of 'article' class into a table which can be written as a CSV
    """
    rows = []
    for article in articles:

        avail = ''
        if not article.available:
            avail = 'x'

        order_number, notifications = validate_string(article.order_number, 'order number', article, notifications)
        name, notifications = validate_string(article.name, 'name', article, notifications)
        note, notifications = validate_string(article.note, 'note', article, notifications)
        manufacturer, notifications = validate_string(article.manufacturer, 'manufacturer', article, notifications)
        origin, notifications = validate_string(article.origin, 'origin', article, notifications)
        unit, notifications = validate_string(article.unit, 'unit', article, notifications)

        article_data = [avail, order_number, name, note, manufacturer, origin, unit, article.price_net, article.vat, article.deposit, article.unit_quantity, '', '', article.category]
        rows.append(article_data)

    return rows, notifications

def compose_articles_csv_message(supplier, foodsoft_url=None, supplier_id=None, categories=[], ignored_categories=[], ignored_subcategories=[], ignored_articles=[], notifications=[], prefix=""):
    text = ""
    if prefix:
        text += prefix + "\n\n"
    text += "Die CSV mit automatisch ausgelesenen Artikeln von " + supplier + " wurde erstellt.\n"
    if foodsoft_url and supplier_id:
        text += "Sie kann unter folgendem Link hochgeladen werden: (Häkchen bei 'Artikel löschen, die nicht in der hochgeladenen Datei sind' setzen!)\n"
        text += foodsoft_url + "suppliers/" + str(supplier_id) + "/articles/upload\n"
    else:
        text += "Sie kann in der Foodsoft hochgeladen werden unter Lieferant -> Artikel -> Artikel hochladen (Häkchen bei 'Artikel löschen, die nicht in der hochgeladenen Datei sind' setzen!)\n"
    if categories:
        text += "\nAusgelesene Kategorien:\n"
        text += base.list_categories(categories)
    if ignored_categories:
        text += "\nIgnorierte Kategorien:\n"
        text += base.list_categories(ignored_categories)
    if ignored_subcategories:
        text += "\nIgnorierte Unterkategorien:\n"
        text += base.list_categories(ignored_subcategories)
    if ignored_articles:
        text += "\nIgnorierte einzelne Artikel:"
        for article in ignored_articles:
            text += "\n#" + str(article.order_number) + " " + article.name + " " + article.unit
            if article.manufacturer:
                text += " von " + article.manufacturer
            if article.origin:
                text += " aus " + article.origin
        text += "\n"
    if notifications:
        text += "\nHinweise:"
        for notification in notifications:
            text += "\n- " + notification
    return text

def write_articles_csv(file_path, articles, notifications=None):
    if not notifications:
        notifications = []
    
    rows, notifications = get_data_from_articles(articles=articles, notifications=notifications)

    with open(file_path + '.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['avail.', 'Order number', 'Name', 'Note', 'Manufacturer', 'Origin', 'Unit', 'Price (net)', 'VAT', 'Deposit', 'Unit quantity', '', '', 'Category'])
        writer.writerows(rows)

    return notifications