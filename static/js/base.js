/**
 * @fileoverview
 * Provides methods for the theme Endpoints sample UI and interaction with the
 * theme Endpoints API.
 */

/** google global namespace for Google projects. */
var google = google || {};

/** appengine namespace for Google Developer Relations projects. */
google.appengine = google.appengine || {};

/** samples namespace for AppEngine sample code. */
google.appengine.samples = google.appengine.samples || {};

/** theme namespace for this sample. */
google.appengine.samples.theme = google.appengine.samples.theme || {};

/**
 * Client ID of the application (from the APIs Console).
 * @type {string}
 */
google.appengine.samples.theme.CLIENT_ID =
    '405390963802-1gkqm09rnc9fhjl6atra67gmnvo6crdi.apps.googleusercontent.com';

/**
 * Scopes used by the application.
 * @type {string}
 */
google.appengine.samples.theme.SCOPES =
    'https://www.googleapis.com/auth/userinfo.email';

/**
 * Whether or not the user is signed in.
 * @type {boolean}
 */
google.appengine.samples.theme.signedIn = false;

/**
 * Loads the application UI after the user has completed auth.
 */
google.appengine.samples.theme.userAuthed = function() {
  var request = gapi.client.oauth2.userinfo.get().execute(function(resp) {
    if (!resp.code) {
      google.appengine.samples.theme.signedIn = true;
      document.querySelector('#signinButton').textContent = 'Sign out';
      document.querySelector('#createMusic').disabled = false;
    }
  });
};

/**
 * Handles the auth flow, with the given value for immediate mode.
 * @param {boolean} mode Whether or not to use immediate mode.
 * @param {Function} callback Callback to call on completion.
 */
google.appengine.samples.theme.signin = function(mode, callback) {
  gapi.auth.authorize({client_id: google.appengine.samples.theme.CLIENT_ID,
      scope: google.appengine.samples.theme.SCOPES, immediate: mode},
      callback);
};

/**
 * Presents the user with the authorization popup.
 */
google.appengine.samples.theme.auth = function() {
  var elems = ['f_getAll', 'f_editMusic', 'f_deleteMusic']
  if (!google.appengine.samples.theme.signedIn) {
    google.appengine.samples.theme.signin(false,
        google.appengine.samples.theme.userAuthed);


    for (var i = elems.length - 1; i >= 0; i--) {
      document.getElementById(elems[i]).style.visibility = "visible";
    };

  } else {
    google.appengine.samples.theme.signedIn = false;
    document.querySelector('#signinButton').textContent = 'Sign in';
    clear_table();
    for (var i = elems.length - 1; i >= 0; i--) {
      document.getElementById(elems[i]).style.visibility = "hidden";
    };
    document.getElementById('musicTable').style.visibility = "hidden";
  }
};

/*
 *Function helping with printing into table
 */
create_and_add = function(type, elem, where){
  var element = document.createElement(type);
  element.innerHTML = elem;
  where.appendChild(element);
};

clear_table = function(){
  var myNode = document.getElementById("outputLog");
  while (myNode.firstChild) {
      myNode.removeChild(myNode.firstChild);
  }
}

/**
 * Prints music into table
 */
google.appengine.samples.theme.print = function(melody) {
  document.getElementById('musicTable').style.visibility = "visible";
  var tr_el = document.createElement('tr');
  create_and_add('td', melody.m_id, tr_el);
  create_and_add('td', melody.name, tr_el);
  create_and_add('td', melody.music_string, tr_el);

  var audio = '<a href="'+ melody.path +'">Download</a>'
  create_and_add('td', audio, tr_el);

  var data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(melody.result));
  var download_json = '<a href="data:' + data + '" download="' + melody.name +'.json">Download JSON</a>'
  create_and_add('td', download_json, tr_el);
  document.querySelector('#outputLog').appendChild(tr_el);
};

/**
 * Gets a numbered melody via the API.
 * @param {string} id ID of the melody.
 */
google.appengine.samples.theme.getMelody = function(id) {
  gapi.client.theme.getMelody({'id': id}).execute(
      function(resp) {
        if (!resp.code) {
          // google.appengine.samples.theme.print(resp);
        }
      });
};

/**
 * Lists Melodies via the API.
 */
google.appengine.samples.theme.listMelodies = function() {
  gapi.client.theme.listMelodies().execute(
      function(resp) {
        if (!resp.code) {
          resp.items = resp.items || [];
          clear_table();
          for (var i = 0; i < resp.items.length; i++) {
            google.appengine.samples.theme.print(resp.items[i]);
          }
        if(resp.items.length == 0){
            document.getElementById('musicTable').style.visibility = "hidden";
          }
        }
      });
};


/**
 * Creates music via the API.
 */
google.appengine.samples.theme.createMusic = function(name, music_string) {
  gapi.client.theme.createMusic({
      'name': name,
      'music_string': music_string
    }).execute(
      function(resp) {
        document.getElementById("errors").innerHTML="";
        if(!resp.error){
          google.appengine.samples.theme.print(resp);
        }
        else{
          document.getElementById("errors").innerHTML=resp.error.message;
        }
      });
};

/**
 * Edit music via the API.
 */
google.appengine.samples.theme.editMusic = function(id, name, music_string){
  gapi.client.theme.editMusic({
    'm_id': id,
    'name': name,
    'music_string': music_string
  }).execute(
    function(resp) {
        document.getElementById("errors_edit").innerHTML="";
        if(!resp.error){
            google.appengine.samples.theme.listMelodies();
        }
        else{
          document.getElementById("errors_edit").innerHTML=resp.error.message;
        }
      });
};

/**
 *Delete music via the API.
 */
google.appengine.samples.theme.deleteMusic = function(id){
  gapi.client.theme.deleteMusic({
    'm_id': id,
  }).execute(
    function(resp) {
        document.getElementById("errors_delete").innerHTML="";
        if(!resp.error){
            google.appengine.samples.theme.listMelodies();
        }
        else{
          document.getElementById("errors_delete").innerHTML=resp.error.message;
        }
      });
};

/**
 * Enables the button callbacks in the UI.
 */
google.appengine.samples.theme.enableButtons = function() {
  var editMusic = document.querySelector('#editMusic');
    editMusic.addEventListener('click', function(e) {
      google.appengine.samples.theme.editMusic(
          document.querySelector('#edit_id').value,
          document.querySelector('#edit_name').value,
          document.querySelector('#edit_music_string').value);
  });

  var listMelodies = document.querySelector('#listMelodies');
  listMelodies.addEventListener('click',
      google.appengine.samples.theme.listMelodies);

  var createMusic = document.querySelector('#createMusic');
  createMusic.addEventListener('click', function(e) {
    google.appengine.samples.theme.createMusic(
        document.querySelector('#name').value,
        document.querySelector('#music_string').value);
  });

  var deleteMusic = document.querySelector('#deleteMusic');
  deleteMusic.addEventListener('click', function(e) {
    google.appengine.samples.theme.deleteMusic(
        document.querySelector('#delete_id').value);
  });

  var signinButton = document.querySelector('#signinButton');
  signinButton.addEventListener('click', google.appengine.samples.theme.auth);
};

/**
 * Initializes the application.
 * @param {string} apiRoot Root of the API's path.
 */
google.appengine.samples.theme.init = function(apiRoot) {
  // Loads the OAuth and theme APIs asynchronously, and triggers login
  // when they have completed.
  var apisToLoad;
  var callback = function() {
    if (--apisToLoad == 0) {
      google.appengine.samples.theme.enableButtons();
    }
  }

  apisToLoad = 2; // must match number of calls to gapi.client.load()
  gapi.client.load('theme', 'v1', callback, apiRoot);
  gapi.client.load('oauth2', 'v2', callback);
};
