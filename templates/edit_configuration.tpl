<!DOCTYPE html>
<html>
    <head>
        <title>{{foodcoop}} Lieferscraping - {{configuration}}</title>
        % include("templates/header.tpl")
    </head>

    <body>
        <div>
            <form action="/{{fc}}"><input type='submit' value='Zurück zum Hauptmenü'></form>
            <p>{{messages}}</p>
            <h1>{{configuration}} Konfiguration</h1>
            <form action="/{{fc}}/{{configuration}}" method="post">
                <label>{{base_locales["configuration name"]}}: <input name="configuration name" type="text" value="{{configuration}}" disabled></label><br/>
                <label>{{base_locales["Script name"]}}: 
                    <select name="Script name" required>
                        {{!script_options}}
                    </select>
                </label><br/>
                <label>{{base_locales["number of runs to list"]}}: <input name="number of runs to list" type="number" value="{{number_of_runs_to_list}}" required></label><br/>
                {{!config_content}}
                <br><br>
                <input type="submit" value="Speichern">
            </form>
            <form action="/{{fc}}/{{configuration}}"><input type='submit' value='Bearbeiten abbrechen'></form>
        </div>
    </body>
</html>