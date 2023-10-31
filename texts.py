TEXTS = {
    "intro": {
        "English": "You can backup your Mush account with this app. Connect to Twinoid to proceed.",
        "Français": "Vous pouvez sauvegarder votre compte Mush avec cette application. Connectez-vous à Twinoid pour continuer."
    },
    "title": {
        "English": "Save Mush Data",
        "Français": "Sauvegarde des données Mush"
    },
    "connectToTwinoid": {
        "English": "Connect to Twinoid",
        "Français": "Se connecter à Twinoid"
    },
    "profileToSave": {
        "English": "Profile to save",
        "Français": "Profil à sauvegarder"
    },
    "getMyMushData": {
        "English": "Get my data!",
        "Français": "Récupérer mes données !"
    },
    "gettingData": {
        "English": "Getting data...",
        "Français": "Récupération des données..."
    },
    "dataRetrieved": {
        "English": "Data successfully retrieved!",
        "Français": "Données récupérées avec succès !"
    },
    "savingData": {
        "English": "Saving data...",
        "Français": "Sauvegarde des données..."
    },
    "congratulations": {
        "English": "Congratulations! Your profile has been successfully saved! Here is a preview of your data:",
        "Français": "Félicitations ! Votre profil a été sauvegardé avec succès ! Voici un aperçu de vos données :"
    },
    "tutorial": {
        "English": """You can backup your Mush account with this app.

Here is the list of items saved :
- Your Twinoid username
- Your achievements and titles
- Your ships

You can additionally save :
- Your character levels
- Your klix

If you fill the "Cookie" field. Please watch the video below to know how to get your cookie.

You can only backup the profile from **one server**. Choose wisely! 

Do not leave the page during the profile import!

It's possible to make as many imports as you want. Please use "Connect to Twinoid" link each time you want to import a new profile.

If you have any question or encounter issues, feel free to contact us on the [Eternaltwin Discord](https://discord.gg/Kd8DUkWy4N).""",
        "Français": """Vous pouvez sauvegarder votre compte Mush avec cette application.

Voici la liste des éléments sauvegardés :
- Votre nom d'utilisateur Twinoid
- Vos réalisations et titres
- Vos vaisseaux

Vous pouvez également sauvegarder :
- Les niveaux de votre personnage
- Vos klix

Si vous remplissez le champ "Cookie". Veuillez regarder la vidéo ci-dessous pour savoir comment obtenir votre cookie.

Vous ne pouvez sauvegarder le profil que depuis **un seul serveur**. Choisissez judicieusement !

Ne quittez pas la page pendant l'importation du profil !

Il est possible de faire autant d'importations que vous le souhaitez. Veuillez utiliser le lien "Se connecter à Twinoid" à chaque fois que vous souhaitez importer un nouveau profil.

Si vous avez des questions ou rencontrez des problèmes, n'hésitez pas à nous contacter sur le [Discord Eternaltwin](https://discord.gg/Kd8DUkWy4N)."""
},
}

def translate(text: str, language: str = "English") -> str:
    return TEXTS[text][language]