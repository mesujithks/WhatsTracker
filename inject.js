// this is the code which will be injected into a given page...
(function () {
  function isMyScriptLoaded(url) {
    if (!url) url = "http://xxx.co.uk/xxx/script.js";
    var scripts = document.getElementsByTagName("script");
    for (var i = scripts.length; i--; ) {
      if (scripts[i].src == url) return true;
    }
    return false;
  }

  if (
    !isMyScriptLoaded(
      "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"
    )
  ) {
    var script = document.createElement("script");
    script.src =
      "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js";
    /* If you need callback */
    script.onload = script.onreadystatechange = function () {};
    /* end */
    document.body.appendChild(script);

    var currentStatus = false;

    function sendNotification(name, status) {
      let dataObject = {};
      dataObject.user_name = name;
      dataObject.active_time = new Date().toLocaleString();
      dataObject.online_status = status;
      console.log(dataObject);
      $.ajax({
        type: "POST",
        contentType: "application/json",
        dataType: "application/json",
        data: JSON.stringify(dataObject),
        crossDomain: true,
        url: "http://127.0.0.1:5000//API/notifyAdmin",
        success: function (res) {
          console.log(res);
        },
      });
    }


    var repeat = window.setInterval(function () {

      console.log("checking");

      if(document.getElementsByClassName("_2YPr_ i0jNr").length != 0){
        if(currentStatus == false){
          sendNotification($(document.getElementsByClassName("_21nHd")[0]).first().text(), "true");
          currentStatus = true;
        }
      } else {
        if(currentStatus == true){
          sendNotification($(document.getElementsByClassName("_21nHd")[0]).first().text(), "false");
          currentStatus = false;
        }
      }

    }, 5000);
  }
})();
