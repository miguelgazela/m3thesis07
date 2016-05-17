$(document).ready(function() {


});

function changeRanking(filename, value, path) {

  $.ajax({
    type: "POST",
    url: "http://localhost:3030/messages",
    data: {filename: filename, ranking: value, msg_path: path},
    success: function (response) {

    }
  });

  console.log("STUFF " + filename);
}
