<!DOCTYPE html>
<html>
    <head>
        <title>{{foodcoop}} Lieferscraping - Login</title>
        % include("templates/header.tpl")
    </head>

    <body>
        <div>
            {{messages}}
            <h1>{{foodcoop}} Lieferscraping - Login</h1>
            <p>{{description}}</p>
            <p>Bitte gib deine Zugangsdaten für folgende Foodsoft-Instanz ein:
            <br/><a href="{{foodsoft_login_address}}" target="_blank">{{foodsoft_address}}</a></p>
            <form action="{{request_path}}" method="post">
                {{!submitted_form_content}}
                <p><label>E-Mail: <input name="email" type="email" /></label></p>
                <p><label>Passwort: <input name="password" type="password" /></label></p>
                <p><input value="Anmelden" type="submit" /></p>
            </form>
            <a href="/">Andere Instanz auswählen</a>
        </div>
    </body>
</html>