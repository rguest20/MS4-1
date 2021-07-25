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

function companyLookup() {
  var query = document.querySelector('.companies');
  var id;
  var ticketoutput = [];
  var ticketoutputoutstanding = [];
  var output = document.querySelector('.ticket');
  var thisclient;
  clients.forEach((client, i) => {
    if (client.fields.client_name === query.value) {
      thisclient = client;
      id = client.pk;
    }
  });
  tickets.forEach((ticket, i) => {
    if (ticket.fields.client === id) {
      ticketoutput.push(ticket);
    }
  });
  ticketoutput.forEach((ticket, i) => {
    if (ticket.fields.resolved === false) {
      ticketoutputoutstanding.push(ticket);
    }
  });
  document.querySelector('#company-name').append(thisclient.fields.client_name);
  document.querySelector('#registered').append(thisclient.fields.contract_start_date.slice(0, 10));
  document.querySelector('#contract').append(thisclient.fields.contracted_monthly_SEM_hours + thisclient.fields.contracted_monthly_service_hours);
  document.querySelector('#tickets-raised').append(ticketoutput.length);
  document.querySelector('#outstanding-tickets').append(ticketoutputoutstanding.length);
  document.querySelector('#paid_extra_hours').append(thisclient.fields.paid_extra_hours);
  document.querySelector('#hours-worked').append(thisclient.fields.hours_used_this_month);
  document.querySelector('#hours-remaining').append(thisclient.fields.paid_extra_hours + thisclient.fields.contracted_monthly_SEM_hours + thisclient.fields.contracted_monthly_service_hours - thisclient.fields.hours_used_this_month);
  document.querySelector('.hidden').classList.remove('hidden');
  document.querySelector('.enter-company').classList.add('hidden');
}

function refresh() {
  location.reload();
}

function setupStripe() {
  fetch("https://ms4-rguest.herokuapp.com/config").then(result => {
    return result.json();
  }).then(data => {
    // Initialize Stripe.js
    stripe = Stripe(data.publicKey);
  });
}

function updatePrice() {
  hours = document.querySelector('#hours').value;
  target = document.querySelector('#price');
  target.innerHTML = hours * 100;
}