<!DOCTYPE html>
<html>
    <head>
        <title>Lieferscraping - Start</title>
        % include("templates/header.tpl")
    </head>

    <body>
        <div>
            <p>{{messages}}</p>
            <h1>Lieferscraping</h1>
            <p>Mit diesem Tool können Python-Skripte ausgeführt werden, die z.B. den Webshop einer bestimmten Lieferant*in auslesen und daraus die Artikelliste als CSV für den Import in die Foodsoft generieren.</p>
            <p>Jede Foodcoop kann ihre eigenen Skript-Konfigurationen anlegen. Darin werden Variablen festgelegt, wie z.B. welche Artikel nicht eingelesen werden sollen.</p>
            <p>Dazu legt jede Foodcoop ihre eigene Instanz an und innerhalb derer wiederum die Skript-Konfigurationen. Jede Instanz verweist auf eine Foodsoft-Instanz, alle Mitglieder jener Foodsoft-Instanz können sich darin einloggen. (Es sind auch mehrere Instanzen pro Foodsoft möglich.)</p>
            <p><a href="https://github.com/foodcoopsat/krautkoopf_lieferscraping" target="_blank">Zum Github-Repository</a> (dort können weitere Skripte via Pull-Requests hinzugefügt werden)</p>
            <br>
            <h2>Registrierte Instanzen</h2>
            <form action="/" method="post">
                <input name="new instance" value="Neue Instanz anlegen" type="submit" />
            </form>
            <p>{{!instances_content}}</p>
        </div>
    </body>
</html>