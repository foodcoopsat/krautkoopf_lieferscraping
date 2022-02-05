<!DOCTYPE html>
<html>
    <head>
        <title>{{current_instance}} Lieferscraping - Instanz wechseln?</title>
        % include("templates/header.tpl")
    </head>

    <body>
        <div>
            <h1>Instanz wechseln?</h1>
            <p>Du versuchst die Instanz {{requested_instance}} aufzurufen, obwohl du gerade in der Instanz {{current_instance}} angemeldet bist.</p>
            <form action="/{{requested_instance}}" method="post">
                {{!submitted_form_content}}
                <input name="logout" value="Von {{current_instance}} abmelden" type="submit" />
            </form>
            <br>
            <form action="/{{current_instance}}"><input type='submit' value='Abbrechen & zurück zu {{current_instance}}'></form>
        </div>
    </body>
</html>