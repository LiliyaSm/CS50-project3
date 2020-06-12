$(document).ready(function () {


    // add badge for pizzas
    $(".group:contains('Pizza')").append(
        "<span class='badge-pill'>add toppings!</span>"
    );

    //press add to card button
    $(".counter").on("submit", function (e) {

        //  setting up AJAX to pass CSRF token
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== "") {
                var cookies = document.cookie.split(";");
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === name + "=") {
                        cookieValue = decodeURIComponent(
                            cookie.substring(name.length + 1)
                        );
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie("csrftoken");
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
        }
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
        });

        e.preventDefault();
        const card = $(this).closest(".info");
        
        // .data() gets only cached price
        const price = card.attr("data-price");
        const amount = $(this).parent().find(".amount").val();
        const id = card.data("id");
        

        $.post(
            "add_to_cart/",
            { id: id, price: price, amount: amount },
            function (response) {
                console.log(response);
            }
        );
    });


    //choosing price small or large
    $("input[name=type]").on("click", function () {
        //radio button choice
        const type = $(this).val();
        const newPrice = $(this).data("price");
        // change price in text field and in data attr
        $(this).closest("div.info").find(".price").text(newPrice);

        //change data attr
        $(this).closest("div.info").attr("data-price", type);

    });
    

    // filter
    $(".groups .nav-link").on("click", function () {
        // hightlight chosen category on nav bar
        $(".groups").find(".active").removeClass("active");
        $(this).addClass("active");

        const filter = $(this).data("group");
        cards = $(".card");
        if (filter === "All") {
            cards.parent().show();
            return;
        }
        cards.parent().hide();

        const titles = $(".group:contains(" + filter + ")");
        titles.closest(".card").parent().show();
    });



        // counter
    $(".minus").click(function () {
        let $input = $(this).parent().find(".amount");
        let count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        // trigger event change
        $input.change();
        return false;
    });
    $(".plus").click(function () {
        let $input = $(this).parent().find(".amount");
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });




    $("td .amount").change(function () {
        const amount = $(this).val();
        const line_id = $(this).closest("tr").data("id")
        const priceField = $(this).closest("tr").find(".calc_price");

        function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie !== "") {
                    var cookies = document.cookie.split(";");
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (
                            cookie.substring(0, name.length + 1) ===
                            name + "="
                        ) {
                            cookieValue = decodeURIComponent(
                                cookie.substring(name.length + 1)
                            );
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            var csrftoken = getCookie("csrftoken");
            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
            }
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (
                        !csrfSafeMethod(settings.type) &&
                        !this.crossDomain
                    ) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
            });

        $.post("update_cart/", { id: line_id, amount: amount }, function (response) {
            
            priceField.text(parseFloat(response.new_price).toFixed(2));
            $(".total-price").text(parseFloat(response.new_total).toFixed(2));

            console.log(response.new_price, response.new_total);
        });

    });





    $("button.close").click(function () {

        const line_id = $(this).closest("tr").data("id");        
        $(this).closest("tr").remove()

         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie !== "") {
                 var cookies = document.cookie.split(";");
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) === name + "=") {
                         cookieValue = decodeURIComponent(
                             cookie.substring(name.length + 1)
                         );
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         var csrftoken = getCookie("csrftoken");
         function csrfSafeMethod(method) {
             // these HTTP methods do not require CSRF protection
             return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
         }
         $.ajaxSetup({
             beforeSend: function (xhr, settings) {
                 if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                     xhr.setRequestHeader("X-CSRFToken", csrftoken);
                 }
             },
         });


         $.post("delete_item/", { id: line_id}, function (response) {
             $(".total-price").text(parseFloat(response.new_total).toFixed(2));

         });



    })









});
