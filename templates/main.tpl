<!DOCTYPE html>
<html>
    <head>
        <title>{{foodcoop}} Lieferscraping - Hauptmenü</title>
        % include("templates/header.tpl")
    </head>

    <body>
        <div>
            <p>{{messages}}</p>
            <h1>{{foodcoop}} Lieferscraping</h1>
            <h2>{{base_locales["script configurations"]}}</h2>
            <p>{{!configurations}}</p>
            <form action="/{{fc}}" method="post">
                <input name="new configuration" value="Neue Konfiguration anlegen" type="submit" />
            </form>
            <br/>
            <form action="/{{fc}}" method="post">
                <input name="logout" value="Abmelden" type="submit" />
            </form>
        </div>
    </body>
</html>