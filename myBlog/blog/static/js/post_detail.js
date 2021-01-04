  $(function() {
    $( "i" ).click(function() {
      $( "i,span" ).toggleClass( "press", 1000 );
    });
  });

  function post_like(post_id){
    $.post( "like/", function() {
    });
    }
