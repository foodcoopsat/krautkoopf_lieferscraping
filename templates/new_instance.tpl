<!DOCTYPE html>
<html>
    <head>
        <title>Lieferscraping - Neue Instanz</title>
        % include("templates/header.tpl")
    </head>

    <body>
        <div>
            <form action="/"><input type='submit' value='Abbrechen'></form>
            <p>{{messages}}</p>
            <h1>Neue Lieferscraping-Instanz</h1>
            <form action="/" method="post">
                <p><label>Name: <input name="new instance name" type="text" placeholder="meine Foodcoop" value="{{name_value}}" required></label></p>
                <p><label>Beschreibung: <input name="description" type="text" placeholder="optional" value="{{description_value}}"></label></p>
                <p><label>Foodsoft-Webadresse: <input name="foodsoft url" type="url" size=50 placeholder="https://app.foodcoops.at/demo/" value="{{url_value}}" required></label></p>
                <p><label>Bevorzugte Sprache/Gebietsschema: <select name="locale" required>{{!locale_options}}</select></label></p>
                <br><br>
                <input type="submit" value="Instanz anlegen">
            </form>
        </div>
    </body>
</html>