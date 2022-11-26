document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click',  compose_email);

  //my changes below
  document.querySelector('#compose-form').addEventListener('submit', send_email);
  // my changes above

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  const showing = document.querySelector('#emails-view')
  showing.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

fetch('/emails/' + mailbox)
.then(response => response.json())
.then(emails => {
    // Print emails
    //console.log(emails);

    // ... do something else with emails ...
    emails.forEach(email => {
      const space = document.createElement('div');
      space.className = email['read'] ? 'space-read' : 'space-unread';
      document.querySelector('#emails-view').append(space);

      if (mailbox === 'sent') {
      space.innerHTML = `<span class-"receivers col-3">${email.recipients}</span>
      <span class="subject col-6">${email.subject}</span>
        <span class="timestamp col-3">${email.timestamp}</span>`;

        space.addEventListener('click', () => {
          load_email(email.id);
      });
    }
      else {
        space.innerHTML = `<span class-"sender col-3 ">${email.sender}</span>
        <span class="subject col-6">${email.subject}</span>
        <span class="timestamp col-3">${email.timestamp}</span>`;

        space.addEventListener('click', () => {
          load_email(email.id);
        });
      }
});
});
}

// define function for sending email below
function send_email(event) {
  event.preventDefault()

  const recipients = document.querySelector('#compose-recipients').value;
  // const sender = document.querySelector('#compose-sender').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // send this using api
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response =>  load_mailbox('sent'))
  .catch(error => {
    console.log('Error:', error);
  });
}

function load_email(id) {

  // show email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // show email
  const space = document.querySelector('#email-view');

  fetch('/emails/' + id)
  .then(response => response.json())
  .then(email => {
    // Print email
  // console.log(email);

    // ... do something else with email ...
  space.innerHTML = `<p class="sender"><b>From: </b>${email.sender}</p>
  <p class="receivers"><b>To: </b>${email.recipients}</p>
  <p class="subject"><b>Subject: </b>${email.subject}</p>
  <p class="timestamp"><b>TimeStamp: </b><span>${email.timestamp}</span></p>
  <hr>
  <p class="body">${email.body}</p>
  <hr>`;

  // add an archive button
  const archive = document.createElement('button');
  archive.className = 'btn btn-sm btn-outline-primary';
  archive.innerHTML = email['archived'] ? 'Unarchive' : 'Archive';
  space.append(archive);
  archive.addEventListener('click', () => {
    fetch('/emails/' + id, {
      method: 'PUT',
      body: JSON.stringify({
        archived: !email['archived']
      })
    })
    .then(response => load_mailbox('inbox'))
  })

  // add a reply button
  const reply = document.createElement('button');
  reply.className = 'btn btn-sm btn-outline-primary';
  reply.innerHTML = 'Reply';
  space.append(reply);
  reply.addEventListener('click', () => {
    compose_email();
    document.querySelector('#compose-recipients').value = email.sender;
    let sub = email.subject;
    if (!sub.startsWith('Re:')) {
      sub = 'Re: ' + sub;
    }
    document.querySelector('#compose-subject').value = sub;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
  })
  });

  fetch('/emails/' + id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true  
    })
  })
}