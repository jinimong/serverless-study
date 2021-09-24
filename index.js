$(document).ready(function () {
  var dialog = document.querySelector('dialog');
  var showDialogButtons = document.querySelectorAll('.show-dialog');
  dialogPolyfill.registerDialog(dialog);
  showDialogButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      dialog.showModal();
    });
  });
  dialog.querySelector('.close').addEventListener('click', function () {
    dialog.close();
  });
  dialog.querySelector('.print').addEventListener('click', function () {
    print();
  });
});
