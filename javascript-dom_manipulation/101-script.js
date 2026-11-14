#!/usr/bin/node

document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#btn_translate').addEventListener('click', function () {
    const language = document.querySelector('#language_code').value;

    fetch(`https://hellosalut.stefanbohacek.com/?lang=${language}`)
      .then(response => response.json())
      .then(data => {
        document.querySelector('#hello').textContent = data.hello;
      })
      .catch(error => {
        console.error('Error fetching translation:', error);
      });
  });
});
