function sayHello() {
  console.log('hello');
}

function check() {
  var query = document.querySelector('.companies');
  var id;
  var results = [];
  var output = document.querySelector('.ticket');
  clients.forEach((client, i) => {
    if (client.fields.client_name === query.value) {
      id = client.pk;
    }
  });
  tickets.forEach((ticket, i) => {
    if (ticket.fields.client === id) {
      results.push(ticket);
    }
  });
  results.forEach((result, i) => {
    var opt = document.createElement('option');
    opt.value = result.fields.title;
    opt.innerHTML = result.fields.title;
    output.append(opt);
  });
  document.querySelector('.hidden').classList.remove('hidden');
  document.querySelector('.enter-company').classList.add('hidden');
}