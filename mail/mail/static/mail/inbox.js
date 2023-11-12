document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // call function when compose form submitted
  document.querySelector('#compose-form').onsubmit = send_email;
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
  document.querySelector('#emails-view').style.display = 'inline';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  if(mailbox == 'sent')
  {
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {
        console.log(emails);
        for(curr in emails)
        {
          var email = emails[curr]
          
          // check if email has been read 
          if(email.read)
          {
            htmlVal = `<div class="email-item read">
                      <div class="email-email">To:${email.recipients}</div>
                      <div class="email-subject">${email.subject}</div>
                      <div class="email-date">${email.timestamp}</div>
                     </div>`;
          }
          else 
          {
            let curr = email.id;
            console.log("Currently displaying ID " + curr);
            htmlVal = `<div class="email-item notRead" onclick='open_email(curr)'>
                      <div class="email-email">To:${email.recipients}</div>
                      <div class="email-subject">${email.subject}</div>
                      <div class="email-date">${email.timestamp}</div>
                     </div>`;
          }
          
          document.querySelector('#emails-view').innerHTML += htmlVal;
        }
    });
  }
  
}

function send_email() {
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });

  load_mailbox("sent");

  return false;
}

function open_email(id)
{
  console.log("Inside open email");

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'inline';
  document.querySelector('#compose-view').style.display = 'none';

  console.log("ID: " + id);

  // Show the mailbox name
  // document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}