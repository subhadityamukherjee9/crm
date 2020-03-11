(function($) {
  $('#lazyLoadLink').on('click', function() {
    var link = $(this);
    var page = link.data('page');
    var search = null;
    if(window.location.href.indexOf("=") > -1) {
        var search = window.location.href
        var search = search.substring(search.indexOf("=") + 1, );
        }
    $.ajax({
      type: 'post',
      url: '/dashboard/lazy_load_posts',
      data: {
        'page': page,
        'search' : search,
        'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
      },
      success: function(data) {
        // if there are still more pages to load,
        // add 1 to the "Load More Posts" link's page data attribute
        // else hide the link
        if (data.has_next) {
            link.data('page', page+1);
        } else {
          link.hide();
        }
        // append html to the posts div
        $('#posts').append(data.posts_html);
      },
      error: function(xhr, status, error) {
        // shit happens friends!
      }
    });
  });
}(jQuery));

$("form#file").submit(function(e) {
    e.preventDefault();
    var formData = new FormData(this);

    $.ajax({
        url: '/dashboard/csv/upload/',
        type: 'POST',
        data: formData,
        beforeSend: function() {
        $('form#file').html("<div class='loaders'><div class='loader circle-loader-1'></div></div>");
        $('#uploadmax').html("CSV file is uploading, we will notify you once it is done.");
          },
        success: function (data) {
          $('#uploadmax').html("CSV file uploaded, Contacts added.");
          if(confirm(data.upload + " Contact Uploaded!")){
            window.location.reload();
          }
        },
        cache: false,
        contentType: false,
        processData: false
    });
});
