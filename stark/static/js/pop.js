

    var pop_back_id="";

    function pop(url,id) {
        pop_back_id=id;
        console.log(pop_back_id);
        window.open(url+'?pop=1','newwindow','width=800,height=500,top=100,left=100,toolbar =no, menubar=no, scrollbars=no, resizable=no, location=no, status=no')

    }

    function pop_back_func(text,pk) {

        console.log(pop_back_id);
        console.log(text,pk);

        var $option=$("<option>"); //  <option></option>
        $option.html(text);
        $option.attr("value",pk);
        $option.attr("selected","selected");

        $("#"+pop_back_id).append($option)
    }
