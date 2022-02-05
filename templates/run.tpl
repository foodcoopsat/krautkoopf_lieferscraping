<!DOCTYPE html>
<html>
    <head>
        <title>{{foodcoop}} Lieferscraping - {{configuration}} - {{run.name}}</title>
        % include("templates/header.tpl")
    </head>

    <body>
        <div>
            <form action="/{{fc}}"><input type='submit' value='Zurück zum Hauptmenü'></form>
            <p>{{messages}}</p>
            <form action="/{{fc}}/{{configuration}}"><input type='submit' value='Zurück zu {{configuration}}'></form>
            <h1>{{configuration}} - Ausführung {{run.name}}</h1>
            <p>{{log_text}}</p>
            <p><label for="run">Fortschritt: </label><progress id="run" value="{{completion_percentage}}" max="100"/></p>
            {{!downloads}}
            {{!continue_content}}
            {{!display_content}}
        </div>
    </body>
</html>