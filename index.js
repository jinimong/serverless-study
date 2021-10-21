$(document).ready(function () {
  var dialog = document.querySelector('dialog');
  dialogPolyfill.registerDialog(dialog);
  dialog.querySelector('.close').addEventListener('click', function () {
    dialog.close();
  });
  dialog.querySelector('.print').addEventListener('click', function () {
    print();
  });

  function load_data() {
    $.ajax({
      url: 'https://8n8ddetmf2.execute-api.ap-northeast-2.amazonaws.com/dev/conference/users/*',
      method: 'get',
      success: function (res) {
        $('#history').empty();
        res.items.forEach((item) => {
          $('#history').append(`
            <li class="mdl-list__item mdl-list__item--three-line">
              <span class="mdl-list__item-primary-content">
                <i class="material-icons mdl-list__item-avatar">person</i>
                <span>${item.user_name}</span>
                <span class="mdl-list__item-text-body"
                  >From ${item.company_name}</span
                >
              </span>
              <span class="mdl-list__item-secondary-content">
                <a
                  class="show-dialog mdl-list__item-secondary-action"
                  href="#"
                  data-user_id="${item.user_id}"
                  data-type="${item.type}"
                  ><i class="material-icons">print</i></a
                >
              </span>
            </li>
          `);
        });
        var showDialogButtons = document.querySelectorAll('.show-dialog');
        showDialogButtons.forEach(function (button) {
          button.addEventListener('click', function (e) {
            e.preventDefault();
            const user_id = $(this).data('user_id');
            const type = $(this).data('type');
            $('#showBox').append(`
              <img style="width: 100%" src="https://jinimong-serverless.s3.ap-northeast-2.amazonaws.com/qrcodes/${user_id}/${type}/qrcode.jpg" />
            `);
            dialog.showModal();
          });
        });
      },
    });
  }

  $('#submitBtn').on('click', function () {
    const form = document.getElementById('postForm');
    const formData = new FormData(form);
    $.ajax({
      url: 'https://8n8ddetmf2.execute-api.ap-northeast-2.amazonaws.com/dev/conference',
      method: 'post',
      datatype: 'json',
      data: JSON.stringify(Object.fromEntries(formData)),
      success: function (res) {
        console.log(res);
        load_data();
      },
    });
  });

  load_data();
});
