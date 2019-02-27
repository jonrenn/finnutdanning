$("select").mousedown(function(e){
    e.preventDefault();

    var select = this;
    var scroll = select .scrollTop;

    e.target.selected = !e.target.selected;

    setTimeout(function(){select.scrollTop = scroll;}, 0);

    $(select ).focus();
}).mousemove(function(e){e.preventDefault()});

function filtersearch(txtFilter) {
    interests = document.getElementById("id_interesser").children;
    for(var i = 0; i < interests.length; i++) {
        if(interests[i].innerHTML.toLowerCase().startsWith(txtFilter.value.toLowerCase()) || interests[i].selected == true) {
            interests[i].style.display = "block";
        }
        else {
            interests[i].style.display = "none";
        }
    }
}
