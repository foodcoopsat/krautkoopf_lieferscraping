<!DOCTYPE html>
<html>
    <head>
        <title>{{foodcoop}} Lieferscraping - {{configuration}} löschen</title>
        % include("templates/header.tpl")
    </head>

    <body>
        <div>
            <form action="/{{fc}}"><input type='submit' value='Zurück zum Hauptmenü'></form>
            <p>{{messages}}</p>
            <h1>Konfiguration {{configuration}} löschen?</h1>
            <p>Achtung, dadurch werden alle Daten dieser Konfiguration unwiderruflich gelöscht!</p>
            <form action="/{{fc}}" method="post">
                <input name="delete configuration" value="{{configuration}}" hidden>
                <input type="submit" value="Löschen bestätigen">
            </form>
            <form action="/{{fc}}/{{configuration}}"><input type='submit' value='Abbrechen'></form>
        </div>
    </body>
</html>