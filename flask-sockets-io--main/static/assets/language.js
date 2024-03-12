// language.js

// Define an object to hold language-specific content
window.languageContent = {
   'english': {
       welcomeText1: 'WELCOME TO SPEAKEASY',
       projectText: 'Project: English-French Translator',
       connectButton: 'CONNECT WITH FRIENDS',
       welcomeText2: 'WELCOME TO KENYA',
       worldText: 'ONE WORLD',
       countryText: 'ONE COUNTRY', 
       signIn: 'SIGN IN',
       chatRoom: 'CHAT ROOM',
       userNamePlaceholder: 'Enter your username',
       roomCodePlaceholder: 'Enter your room code',
       joinBtn: 'Join a Room',
       createBtn: 'Create a Room',
       chatTitle: 'Live Chat',
       chatInvitation: 'Chat Invitation Code:',
       leaveChat: 'Leave Chat',
       messagePlaceholder: 'Message',
       sendBtn: 'Send'
   },
   'french': {
       welcomeText1: 'BIENVENUE À SPEAKEASY',
       projectText: 'Projet : Traducteur Anglais-Français',
       connectButton: 'CONNECTEZ-VOUS AVEC DES AMIS',
       welcomeText2: 'BIENVENUE AU KENYA',
       worldText:'UN SEUL MONDE ',
       countryText: 'UN PAYS',
       signIn: 'OUVRIR UNE SESSION',
       chatRoom: 'SALLE DE PARLER',
       userNamePlaceholder: 'Entrez votre nom d\'utilisateur',
       roomCodePlaceholder: 'Entrez le code de votre chambre',
       joinBtn: 'Rejoindre une salle',
       createBtn: 'Créer une salle',
       chatTitle: 'Chat en direct',
       chatInvitation: 'Code d\'invitation au chat:',
       leaveChat: 'Quitter le chat',
       messagePlaceholder: 'Message',
       sendBtn: 'Envoyer'
   },
   'swahili': {
       welcomeText1: 'KARIBU SPEAKEASY',
       projectText: 'Mradi: Mtafsiri wa Kiingereza-Kiswahili',
       connectButton: 'UNGANA NA MARAFIKI',
       welcomeText2: 'KARIBU KENYA',
       worldText: 'DUNIA MOJA',
       countryText: 'NCHI MOJA',
       signIn: 'KUINGIA',
       chatRoom: 'CHUMBA CHA MAZUNGUMZO',
       userNamePlaceholder: 'Ingiza jina lako',
       roomCodePlaceholder: 'Ingiza msimbo wa chumba chako',
       joinBtn: 'Jiunge na chumba',
       createBtn: 'Unda Chumba',
       chatTitle: 'Mazungumzo Moja kwa moja',
       chatInvitation: 'Nambari ya Mwaliko wa Mazungumzo:',
       leaveChat: 'Ondoka kwenye Mazungumzo',
       messagePlaceholder: 'Ujumbe',
       sendBtn: 'Tuma'
   }
};

window.changeLanguage = function(language) {
   // Set the selected language in a cookie
   document.cookie = `selectedLanguage=${language}; expires=Fri, 31 Dec 9999 23:59:59 GMT; SameSite=None; Secure`;

   // Update the content on the page based on the selected language
   const selectedContent = window.languageContent[language];

   console.log('Selected Content:', selectedContent); // Log selectedContent to the console

   const updateElementText = (elementId, contentKey) => {
      const element = document.getElementById(elementId);
      if (element) {
         element.innerText = selectedContent[contentKey];
      } else {
         console.error(`Element with ID "${elementId}" not found.`);
      }
   };

   const updateElementPlaceholder = (elementId, placeholderKey) => {
      const element = document.getElementById(elementId);
      if (element) {
         // Check if the element is an input element with a placeholder attribute
         if (element.tagName === 'INPUT' && element.hasAttribute('placeholder')) {
            element.setAttribute('placeholder', selectedContent[placeholderKey]);
         } else {
            console.error(`Element with ID "${elementId}" is not an input element or does not have a placeholder attribute.`);
         }
      } else {
         console.error(`Element with ID "${elementId}" not found.`);
      }
   };

   // Update individual elements
   updateElementText('welcomeText1', 'welcomeText1');
   updateElementText('projectText', 'projectText');
   updateElementText('connectButton', 'connectButton');
   updateElementText('welcomeText2', 'welcomeText2');
   updateElementText('worldText', 'worldText');
   updateElementText('countryText', 'countryText');
   updateElementText('signIn', 'signIn');
   updateElementText('chatRoom', 'chatRoom');
   updateElementText('userNamePlaceholder', 'userNamePlaceholder');
   updateElementText('roomCodePlaceholder', 'roomCodePlaceholder');
   updateElementText('joinBtn', 'joinBtn');
   updateElementText('createBtn', 'createBtn');
   updateElementText('chatTitle', 'chatTitle');
   updateElementText('chatInvitation', 'chatInvitation');
   updateElementText('leaveChat', 'leaveChat');
   updateElementText('messagePlaceholder', 'messagePlaceholder');
   updateElementText('sendBtn', 'sendBtn');

   // Update placeholders for input elements
   updateElementPlaceholder('userNamePlaceholder', 'userNamePlaceholder');
   updateElementPlaceholder('roomCodePlaceholder', 'roomCodePlaceholder');

   // Add more calls to updateElementPlaceholder for other input elements as needed
};

window.addEventListener('DOMContentLoaded', () => {
   const languageCookie = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage='));
   const selectedLanguage = languageCookie ? languageCookie.split('=')[1] : 'english'; // Default to 'english' if no cookie is found
   changeLanguage(selectedLanguage);
});
