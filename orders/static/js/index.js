$(document).ready(function () {

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


    // add badge for pizzas
    $(".type:contains('topping')")
        .parent()
        .append("<span class='badge-pill'>add toppings!</span>");

    //  add to cart dish with topping
    $(".cart-toppings").on("submit", function (e) {
        e.preventDefault();
        const card = $(this).closest(".info");

        // get price type, use attr because.data() gets only cached price
        const price = card.attr("data-price");
        const id = card.data("id");

        //get topping info
        const $input = card.find(".amount");
        const $checkbox = card.find("input[type=checkbox]:checked ");
        let dict = {};

        $input.each(function () {
            if ($(this).val() > 0) {
                idtop = $(this).attr("data-idtop");
                dict[idtop] = $(this).val();
            }
        });

        $checkbox.each(function () {
            idtop = $(this).attr("data-idtop");
            console.log(idtop);
            dict[idtop] = 1;
        });

        $(this).parent(".toppings").addClass("hide");
        $.post(
            "add_to_cart/",
            { id: id, price: price, toppings: JSON.stringify(dict) },
            function (response) {
                console.log(response);
            }
        );
    });

    //show available toppings for item on the main page
    $(".choose-toppings").on("click", function (e) {
        //get item id and show its toppings
        const card = $(this).closest(".info");
        const id = card.data("id");
        const toppings = $(".toppings").closest(`[data-id = ${id}]`);
        toppings.removeClass("hide");
    });

    //add item without toppings to cart, pressing button
    $(".add-cart").on("submit", function (e) {
        e.preventDefault();
        const card = $(this).closest(".info");
        // use attr because.data() gets only cached price
        const price = card.attr("data-price");
        const id = card.data("id");
        toppings = {};
        $.post(
            "add_to_cart/",
            { id: id, price: price, toppings: toppings },
            function (response) {
                console.log(response);
            }
        );
    });

    //radio size selector (small or large) on main page
    $("input[name=type]").on("click", function () {
        //radio button choice
        const type = $(this).val();
        const newPrice = $(this).data("price");
        // change price in text field and in data attr
        $(this).closest("div.info").find(".price").text(newPrice);
        //change data attr
        $(this).closest("div.info").attr("data-price", type);
    });

    // nav filter on the main page
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

    // counter for pizza toppings

    $(".topMinus").click(function () {
        let $input = $(this).closest(".toppings").find(".topCounter");
        let $allInputs = $(this).closest(".toppings").find(".amount");
        let $inputTop = $(this).parent().find(".amount");
        let count = parseInt($input.val()) - 1;
        if ($input.val() > 0 && $inputTop.val() > 0) {
            count = count < 0 ? 0 : count;
            $input.val(count);
            $allInputs.each(function () {
                let newMax = 4 - $input.val() + parseInt($(this).val());
                $(this).attr("max", newMax);
            });
            // trigger event change
            $input.change();
            return false;
        }
    });

    $(".minus").click(function () {
        let $input = $(this).parent().find(".amount");
        const minValue = $input.attr("min");
        let count = parseInt($input.val()) - 1;
        count = count < minValue ? minValue : count;
        $input.val(count);
        // trigger event change
        $input.change();
        return false;
    });
    $(".plus").click(function () {
        let $input = $(this).parent().find(".amount");
        const maxValue = $input.attr("max");
        let count = parseInt($input.val()) + 1;
        count = count > maxValue ? maxValue : count;
        $input.val(count);
        $input.change();
        return false;
    });

    $(".topPlus").click(function () {
        let $input = $(this).closest(".toppings").find(".topCounter");
        let $allInputs = $(this).closest(".toppings").find(".amount");
        if ($input.val() < 4) {
            $input.val(parseInt($input.val()) + 1);
            $input.change();
            $allInputs.each(function () {
                let newMax = 4 - $input.val() + parseInt($(this).val());
                $(this).attr("max", newMax);
            });
            return false;
        }
    });

    //if changes amount it will change price and total sum in the cart
    $("td .amount").change(function () {
        const amount = $(this).val();
        const line_id = $(this).closest("tr").data("id");
        const priceField = $(this).closest("tr").find(".calc_price");

        $.post("update_cart/", { id: line_id, amount: amount }, function (
            response
        ) {
            //set new new item * amount (calculated) price and total price
            priceField.text(parseFloat(response.new_price).toFixed(2));
            $(".total-price").text(parseFloat(response.new_total).toFixed(2));
        });
    });

    // close toppings window 
    $(".toppings .close").click(function () {
        $(this).parent(".toppings").addClass("hide");
    });

    // delete item from cart
    $(".cart.close").click(function () {
        const line_id = $(this).closest("tr").data("id");
        $(this).closest("tr").remove();

        $.post("delete_item/", { id: line_id }, function (response) {
            $(".total-price").text(parseFloat(response.new_total).toFixed(2));
            if (response.last_one) {
                $(".confirm-cart").addClass("hide");
                $(".container")
                    .first()
                    .append("<h4 class='text-center'>Your cart is empty</h4>");
            }
        });
    });
});
